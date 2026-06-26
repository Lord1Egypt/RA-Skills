"""
Verification engine for Bridge tasks.

Validates proof submissions against formal criteria.
Each proof type has a deterministic verification function.
"""

import math

from .models import CriterionResult, ProofItem, VerificationCriterion


def _haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate distance in meters between two GPS coordinates."""
    R = 6371000  # Earth radius in meters
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def verify_gps_proof(criterion: VerificationCriterion, proof: ProofItem) -> CriterionResult:
    """Verify worker was at the required location."""
    params = criterion.params
    proof_data = proof.data

    required_lat = float(params.get("latitude", 0))
    required_lon = float(params.get("longitude", 0))
    radius_m = float(params.get("radius_m", 100))

    submitted_lat = float(proof_data.get("latitude", 0))
    submitted_lon = float(proof_data.get("longitude", 0))

    distance = _haversine(required_lat, required_lon, submitted_lat, submitted_lon)
    passed = distance <= radius_m

    return CriterionResult(
        type="gps_proof",
        passed=passed,
        detail=f"Distance: {distance:.0f}m (max: {radius_m:.0f}m)",
    )


def verify_photo_proof(criterion: VerificationCriterion, proof: ProofItem) -> CriterionResult:
    """Verify required number of photos submitted with unique hashes."""
    min_photos = int(criterion.params.get("min_photos", 1))
    hashes = proof.data.get("photo_hashes", [])
    unique_hashes = set(hashes)

    passed = len(unique_hashes) >= min_photos

    return CriterionResult(
        type="photo_proof",
        passed=passed,
        detail=f"Photos: {len(unique_hashes)} unique (min: {min_photos})",
    )


def verify_timestamp_proof(criterion: VerificationCriterion, proof: ProofItem) -> CriterionResult:
    """Verify task completed within time limit."""
    max_hours = float(criterion.params.get("max_hours", 24))

    accepted = proof.data.get("accepted_at", "")
    completed = proof.data.get("completed_at", "")

    if not accepted or not completed:
        return CriterionResult(type="timestamp_proof", passed=False, detail="Missing timestamps")

    # Simple hour calculation from ISO strings
    from datetime import datetime
    try:
        t_accepted = datetime.fromisoformat(accepted.replace("Z", "+00:00"))
        t_completed = datetime.fromisoformat(completed.replace("Z", "+00:00"))
        elapsed_hours = (t_completed - t_accepted).total_seconds() / 3600
        passed = elapsed_hours <= max_hours
        return CriterionResult(
            type="timestamp_proof",
            passed=passed,
            detail=f"Elapsed: {elapsed_hours:.1f}h (max: {max_hours:.1f}h)",
        )
    except (ValueError, TypeError):
        return CriterionResult(type="timestamp_proof", passed=False, detail="Invalid timestamp format")


def verify_signature_proof(criterion: VerificationCriterion, proof: ProofItem) -> CriterionResult:
    """Verify cryptographic signature is present (simplified — checks non-empty)."""
    signature = proof.data.get("signature", "")
    passed = len(signature) > 0
    return CriterionResult(
        type="signature_proof",
        passed=passed,
        detail="Signature present" if passed else "No signature provided",
    )


_VERIFIERS = {
    "gps_proof": verify_gps_proof,
    "photo_proof": verify_photo_proof,
    "timestamp_proof": verify_timestamp_proof,
    "signature_proof": verify_signature_proof,
}


def verify_all(
    criteria: list[VerificationCriterion],
    proofs: list[ProofItem],
) -> tuple[bool, list[CriterionResult]]:
    """Verify all criteria against submitted proofs.

    Returns (all_passed, results).
    """
    proof_by_type = {p.type: p for p in proofs}
    results: list[CriterionResult] = []

    for criterion in criteria:
        proof = proof_by_type.get(criterion.type)
        if proof is None:
            results.append(CriterionResult(
                type=criterion.type,
                passed=False,
                detail=f"No proof submitted for {criterion.type}",
            ))
            continue

        verifier = _VERIFIERS.get(criterion.type)
        if verifier is None:
            results.append(CriterionResult(
                type=criterion.type,
                passed=False,
                detail=f"Unknown proof type: {criterion.type}",
            ))
            continue

        results.append(verifier(criterion, proof))

    all_passed = all(r.passed for r in results)
    return all_passed, results
