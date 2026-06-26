"""Regenerate E2EE keys for an existing DID identity.

When a credential file is missing E2EE private keys (e2ee_signing_private_pem,
e2ee_agreement_private_pem), this script generates new key-2 (secp256r1) and
key-3 (X25519) key pairs, updates the DID document with new public keys,
re-signs the document with key-1, calls did-auth.update_document on the server,
and saves everything locally.

Usage:
    python scripts/regenerate_e2ee_keys.py --credential default

[INPUT]: credential_store (load/save), ANP (_build_e2ee_entries, generate_w3c_proof),
         utils.auth (update_did_document, get_jwt_via_wba), utils.config (SDKConfig),
         logging_config
[OUTPUT]: Updated credential file with E2EE private keys and refreshed DID document
[POS]: CLI script for E2EE key recovery; one-time repair tool

[PROTOCOL]:
1. Update this header when logic changes
2. Check the folder's CLAUDE.md after updates
"""

import argparse
import asyncio
import copy
import logging
import secrets
import sys

from utils import (
    SDKConfig,
    create_user_service_client,
    update_did_document,
    get_jwt_via_wba,
)
from utils.identity import DIDIdentity, load_private_key
from utils.logging_config import configure_logging
from credential_store import load_identity, save_identity

# ANP internals for E2EE key generation and proof signing
from anp.authentication.did_wba import _build_e2ee_entries
from anp.proof.proof import generate_w3c_proof

logger = logging.getLogger(__name__)


async def regenerate_e2ee_keys(
    credential_name: str = "default",
    force: bool = False,
) -> None:
    """Regenerate E2EE keys for an existing credential.

    Steps:
        1. Load existing credential and verify key-1 exists
        2. Generate new key-2 (secp256r1) and key-3 (X25519) via ANP
        3. Update DID document: replace key-2/key-3 entries, update keyAgreement, re-sign
        4. Update the DID document on the server and refresh JWT
        5. Save updated credential locally
    """
    logger.info("Regenerating E2EE keys credential=%s force=%s", credential_name, force)
    # Step 1: Load existing credential
    data = load_identity(credential_name)
    if data is None:
        print(f"Error: Credential '{credential_name}' not found.")
        print(
            "Create an identity first: python scripts/setup_identity.py --name MyAgent"
        )
        sys.exit(1)

    did = data["did"]
    print(f"Loaded credential: {credential_name}")
    print(f"  DID: {did}")

    # Check if E2EE keys already exist
    has_signing = bool(data.get("e2ee_signing_private_pem"))
    has_agreement = bool(data.get("e2ee_agreement_private_pem"))
    if has_signing and has_agreement:
        if not force:
            print("\n  E2EE keys already present in credential.")
            print("  Use --force to regenerate anyway.")
            sys.exit(0)
        print("\n  --force specified, regenerating existing E2EE keys...")

    # Verify key-1 private key exists (needed for re-signing)
    private_key_pem = data.get("private_key_pem")
    if not private_key_pem:
        print("Error: key-1 private key not found in credential. Cannot re-sign.")
        sys.exit(1)

    if isinstance(private_key_pem, str):
        private_key_pem = private_key_pem.encode("utf-8")

    private_key = load_private_key(private_key_pem)
    print("  key-1 private key: OK")

    # Step 2: Generate new E2EE keys
    print("\nGenerating new E2EE keys...")
    e2ee_vms, ka_refs, e2ee_keys = _build_e2ee_entries(did)
    e2ee_signing_private_pem = e2ee_keys["key-2"][0]
    e2ee_agreement_private_pem = e2ee_keys["key-3"][0]
    print("  key-2 (secp256r1 signing): generated")
    print("  key-3 (X25519 agreement): generated")

    # Step 3: Update DID document
    print("\nUpdating DID document...")
    did_document = data.get("did_document")
    if not did_document:
        print("Error: DID document not found in credential.")
        sys.exit(1)

    did_document = copy.deepcopy(did_document)

    # Replace key-2 and key-3 in verificationMethod
    vm_list = did_document.get("verificationMethod", [])
    # Remove old key-2 and key-3 entries
    vm_list = [
        vm
        for vm in vm_list
        if not (
            vm.get("id", "").endswith("#key-2") or vm.get("id", "").endswith("#key-3")
        )
    ]
    # Add new key-2 and key-3 entries
    vm_list.extend(e2ee_vms)
    did_document["verificationMethod"] = vm_list

    # Update keyAgreement references
    did_document["keyAgreement"] = ka_refs

    # Ensure x25519 context is present
    contexts = did_document.get("@context", [])
    x25519_ctx = "https://w3id.org/security/suites/x25519-2019/v1"
    if x25519_ctx not in contexts:
        contexts.append(x25519_ctx)
        did_document["@context"] = contexts

    # Remove old proof before re-signing
    did_document.pop("proof", None)

    # Re-sign with key-1
    verification_method = f"{did}#key-1"
    did_document = generate_w3c_proof(
        document=did_document,
        private_key=private_key,
        verification_method=verification_method,
        proof_purpose="authentication",
        domain=SDKConfig().did_domain,
        challenge=secrets.token_hex(16),
    )
    print("  DID document re-signed with key-1")

    # Step 4: Update DID document on server and refresh JWT
    config = SDKConfig()
    print("\nUpdating DID document on server...")
    print(f"  Server: {config.user_service_url}")

    # Build a DIDIdentity for registration
    public_key_pem = data.get("public_key_pem", "")
    if isinstance(public_key_pem, str):
        public_key_pem = public_key_pem.encode("utf-8")

    identity = DIDIdentity(
        did=did,
        did_document=did_document,
        private_key_pem=private_key_pem,
        public_key_pem=public_key_pem,
        user_id=data.get("user_id"),
        jwt_token=data.get("jwt_token"),
        e2ee_signing_private_pem=e2ee_signing_private_pem,
        e2ee_agreement_private_pem=e2ee_agreement_private_pem,
    )

    async with create_user_service_client(config) as client:
        update_result = await update_did_document(
            client,
            identity,
            config.did_domain,
        )
        print(f"  Update: {update_result.get('message', 'OK')}")
        identity.user_id = update_result.get("user_id", identity.user_id)

        # Refresh JWT (or reuse the token returned by update_document)
        jwt_token = update_result.get("access_token")
        if not jwt_token:
            jwt_token = await get_jwt_via_wba(client, identity, config.did_domain)
        identity.jwt_token = jwt_token
        print(f"  JWT refreshed: {jwt_token[:50]}...")

    # Step 5: Save updated credential
    path = save_identity(
        did=identity.did,
        unique_id=data.get("unique_id", identity.unique_id),
        user_id=identity.user_id,
        private_key_pem=identity.private_key_pem,
        public_key_pem=identity.public_key_pem,
        jwt_token=identity.jwt_token,
        display_name=data.get("name"),
        handle=data.get("handle"),
        name=credential_name,
        did_document=identity.did_document,
        e2ee_signing_private_pem=identity.e2ee_signing_private_pem,
        e2ee_agreement_private_pem=identity.e2ee_agreement_private_pem,
    )
    print(f"\nCredential saved to: {path}")
    print("E2EE key regeneration complete!")


def main() -> None:
    configure_logging(console_level=None, mirror_stdio=True)

    parser = argparse.ArgumentParser(
        description="Regenerate E2EE keys for an existing DID identity"
    )
    parser.add_argument(
        "--credential",
        type=str,
        default="default",
        help="Credential name (default: default)",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Force regeneration even if E2EE keys already exist",
    )
    args = parser.parse_args()
    logger.info(
        "regenerate_e2ee_keys CLI started credential=%s force=%s",
        args.credential,
        args.force,
    )
    asyncio.run(regenerate_e2ee_keys(args.credential, force=args.force))


if __name__ == "__main__":
    main()
