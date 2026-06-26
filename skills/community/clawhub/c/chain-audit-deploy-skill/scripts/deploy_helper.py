#!/usr/bin/env python3
"""Blockchain contract deployment helper.

Supports Solidity (Foundry), Sui Move, and Solana (Anchor/native) deployments.
Generates and executes deployment commands based on chain type, network,
and user-provided parameters. Outputs JSON results.
"""

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timezone

# ---------------------------------------------------------------------------
# Network configurations
# ---------------------------------------------------------------------------

SOLIDITY_NETWORKS = {
    "mainnet": {"rpc": "https://eth.llamarpc.com", "chain_id": 1, "explorer": "https://etherscan.io"},
    "sepolia": {"rpc": "https://rpc.ankr.com/eth_sepolia", "chain_id": 11155111, "explorer": "https://sepolia.etherscan.io"},
    "holesky": {"rpc": "https://rpc.ankr.com/eth_holesky", "chain_id": 17000, "explorer": "https://holesky.etherscan.io"},
    "bsc": {"rpc": "https://bsc-dataseed.binance.org", "chain_id": 56, "explorer": "https://bscscan.com"},
    "bsc-testnet": {"rpc": "https://data-seed-prebsc-1-s1.binance.org:8545", "chain_id": 97, "explorer": "https://testnet.bscscan.com"},
    "base": {"rpc": "https://mainnet.base.org", "chain_id": 8453, "explorer": "https://basescan.org"},
    "base-sepolia": {"rpc": "https://sepolia.base.org", "chain_id": 84532, "explorer": "https://sepolia.basescan.org"},
    "monad": {"rpc": "https://rpc.monad.xyz", "chain_id": 143, "explorer": "https://monadscan.com"},
    "monad-testnet": {"rpc": "https://testnet-rpc.monad.xyz", "chain_id": 10143, "explorer": "https://testnet.monadscan.com"},
    "0g": {"rpc": "https://evmrpc.0g.ai", "chain_id": 16661, "explorer": "https://chainscan.0g.ai"},
    "0g-testnet": {"rpc": "https://evmrpc-testnet.0g.ai", "chain_id": 16602, "explorer": "https://chainscan-galileo.0g.ai"},
}

SUI_NETWORKS = {
    "mainnet": {"rpc": "https://fullnode.mainnet.sui.io:443", "explorer": "https://suiexplorer.com"},
    "testnet": {"rpc": "https://fullnode.testnet.sui.io:443", "explorer": "https://suiexplorer.com/?network=testnet"},
    "devnet": {"rpc": "https://fullnode.devnet.sui.io:443", "explorer": "https://suiexplorer.com/?network=devnet"},
    "localnet": {"rpc": "http://127.0.0.1:9000", "explorer": ""},
}

SOLANA_NETWORKS = {
    "mainnet-beta": {"rpc": "https://api.mainnet-beta.solana.com", "explorer": "https://explorer.solana.com"},
    "testnet": {"rpc": "https://api.testnet.solana.com", "explorer": "https://explorer.solana.com/?cluster=testnet"},
    "devnet": {"rpc": "https://api.devnet.solana.com", "explorer": "https://explorer.solana.com/?cluster=devnet"},
    "localnet": {"rpc": "http://127.0.0.1:8899", "explorer": ""},
}

MAINNET_NETWORKS = {"mainnet", "mainnet-beta", "bsc", "base", "monad", "0g"}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _which(binary: str) -> str | None:
    for d in os.environ.get("PATH", "").split(os.pathsep):
        p = os.path.join(d, binary)
        if os.path.isfile(p) and os.access(p, os.X_OK):
            return p
    return None


def _run(cmd: list[str], cwd: str, timeout: int = 600) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout)


def _is_mainnet(network: str) -> bool:
    return network in MAINNET_NETWORKS


# ---------------------------------------------------------------------------
# Solidity deployment (Foundry / forge)
# ---------------------------------------------------------------------------

def deploy_solidity(args) -> dict:
    """Deploy Solidity contract using forge."""
    network = args.network or "sepolia"
    net_config = SOLIDITY_NETWORKS.get(network)
    rpc_url = args.rpc_url or (net_config["rpc"] if net_config else None)

    if not rpc_url:
        return {
            "success": False,
            "error": "invalid_network",
            "message": f"Unknown network '{network}'. Supported: {', '.join(SOLIDITY_NETWORKS.keys())}. Or provide --rpc-url.",
        }

    # Build the deployment command
    cmd = ["forge", "create"]

    # If a specific contract is specified
    if args.contract:
        cmd.append(args.contract)

    cmd.extend(["--rpc-url", rpc_url])

    # Private key handling — require env var, never accept raw key
    if args.private_key_env:
        if not args.dry_run:
            key_val = os.environ.get(args.private_key_env)
            if not key_val:
                return {
                    "success": False,
                    "error": "missing_env",
                    "message": f"Environment variable {args.private_key_env} is not set.",
                }
            cmd.extend(["--private-key", key_val])
        else:
            cmd.extend(["--private-key", f"${args.private_key_env}"])
    else:
        # Default to interactive / ledger
        cmd.append("--interactive")

    # Constructor args
    if args.args:
        cmd.extend(["--constructor-args"] + args.args.split())

    # Gas settings
    if args.gas_budget:
        cmd.extend(["--gas-limit", args.gas_budget])

    # Verification
    if args.verify:
        cmd.append("--verify")

    # Dry run
    if args.dry_run:
        return {
            "success": True,
            "dry_run": True,
            "chain": "solidity",
            "network": network,
            "rpc_url": rpc_url,
            "command": " ".join(cmd),
            "message": "Dry run — command generated but not executed.",
        }

    # Check tool availability (only for actual deployment)
    if not _which("forge"):
        return {
            "success": False,
            "error": "tool_not_found",
            "message": "forge (Foundry) is not installed",
            "install_hint": "curl -L https://foundry.paradigm.xyz | bash && foundryup",
        }

    # Execute
    try:
        r = _run(cmd, cwd=args.path, timeout=300)
        output = (r.stdout or "") + "\n" + (r.stderr or "")

        if r.returncode == 0:
            # Try to extract deployed address
            import re
            addr_match = re.search(r"Deployed to:\s*(0x[0-9a-fA-F]+)", output)
            tx_match = re.search(r"Transaction hash:\s*(0x[0-9a-fA-F]+)", output)

            address = addr_match.group(1) if addr_match else "unknown"
            tx_hash = tx_match.group(1) if tx_match else "unknown"
            explorer = net_config.get("explorer", "") if net_config else ""

            return {
                "success": True,
                "chain": "solidity",
                "network": network,
                "contract_address": address,
                "transaction_hash": tx_hash,
                "explorer_url": f"{explorer}/address/{address}" if explorer else "",
                "tx_explorer_url": f"{explorer}/tx/{tx_hash}" if explorer else "",
                "raw_output": output.strip()[:2000],
            }
        else:
            return {
                "success": False,
                "chain": "solidity",
                "network": network,
                "error": "deployment_failed",
                "message": output.strip()[:2000],
                "command": " ".join(cmd),
            }
    except subprocess.TimeoutExpired:
        return {"success": False, "error": "timeout", "message": "Deployment timed out after 300s"}
    except Exception as exc:
        return {"success": False, "error": "execution_failed", "message": str(exc)}


# ---------------------------------------------------------------------------
# Sui Move deployment
# ---------------------------------------------------------------------------

def deploy_sui_move(args) -> dict:
    """Deploy Sui Move package."""
    network = args.network or "testnet"
    net_config = SUI_NETWORKS.get(network)

    if not net_config and not args.rpc_url:
        return {
            "success": False,
            "error": "invalid_network",
            "message": f"Unknown network '{network}'. Supported: {', '.join(SUI_NETWORKS.keys())}. Or provide --rpc-url.",
        }

    rpc_url = args.rpc_url or net_config["rpc"]
    cmd = ["sui", "client", "publish", "--gas-budget", args.gas_budget or "100000000"]

    # Skip dependency verification for faster deploys (optional)
    if args.skip_dependency_verification:
        cmd.append("--skip-dependency-verification")

    # Dry run
    if args.dry_run:
        return {
            "success": True,
            "dry_run": True,
            "chain": "sui_move",
            "network": network,
            "rpc_url": rpc_url,
            "command": " ".join(cmd),
            "message": "Dry run — command generated. Use 'sui client switch --env <network>' to set the active network.",
        }

    # Check tool availability (only for actual deployment)
    if not _which("sui"):
        return {
            "success": False,
            "error": "tool_not_found",
            "message": "sui CLI is not installed",
            "install_hint": "cargo install --locked --git https://github.com/MystenLabs/sui.git sui",
        }

    # Execute
    try:
        # Set env to json output
        env = os.environ.copy()
        r = _run(cmd + ["--json"], cwd=args.path, timeout=300)
        output = (r.stdout or "") + "\n" + (r.stderr or "")

        if r.returncode == 0:
            # Parse JSON output
            json_start = (r.stdout or "").find("{")
            result_data = {}
            if json_start != -1:
                try:
                    result_data = json.loads(r.stdout[json_start:])
                except json.JSONDecodeError:
                    pass

            package_id = "unknown"
            tx_digest = "unknown"

            # Extract from sui publish output
            if "objectChanges" in result_data:
                for change in result_data["objectChanges"]:
                    if change.get("type") == "published":
                        package_id = change.get("packageId", "unknown")
            if "digest" in result_data:
                tx_digest = result_data["digest"]

            explorer = net_config.get("explorer", "") if net_config else ""

            return {
                "success": True,
                "chain": "sui_move",
                "network": network,
                "package_id": package_id,
                "transaction_digest": tx_digest,
                "explorer_url": f"{explorer}/object/{package_id}" if explorer and package_id != "unknown" else "",
                "tx_explorer_url": f"{explorer}/txblock/{tx_digest}" if explorer and tx_digest != "unknown" else "",
                "raw_output": output.strip()[:2000],
            }
        else:
            return {
                "success": False,
                "chain": "sui_move",
                "network": network,
                "error": "deployment_failed",
                "message": output.strip()[:2000],
                "command": " ".join(cmd),
            }
    except subprocess.TimeoutExpired:
        return {"success": False, "error": "timeout", "message": "Deployment timed out after 300s"}
    except Exception as exc:
        return {"success": False, "error": "execution_failed", "message": str(exc)}


# ---------------------------------------------------------------------------
# Solana deployment
# ---------------------------------------------------------------------------

def deploy_solana(args) -> dict:
    """Deploy Solana program (Anchor or native)."""
    is_anchor = os.path.exists(os.path.join(args.path, "Anchor.toml"))

    network = args.network or "devnet"
    net_config = SOLANA_NETWORKS.get(network)

    if not net_config and not args.rpc_url:
        return {
            "success": False,
            "error": "invalid_network",
            "message": f"Unknown network '{network}'. Supported: {', '.join(SOLANA_NETWORKS.keys())}. Or provide --rpc-url.",
        }

    rpc_url = args.rpc_url or net_config["rpc"]

    if is_anchor:
        cmd = ["anchor", "deploy", "--provider.cluster", rpc_url]
        if args.program_id:
            cmd.extend(["--program-id", args.program_id])
    else:
        cmd = ["solana", "program", "deploy", "<COMPILED_PROGRAM.so>"]
        cmd.extend(["--url", rpc_url])
        if args.keypair:
            cmd.extend(["--keypair", args.keypair])
        if args.program_id:
            cmd.extend(["--program-id", args.program_id])

    # Dry run
    if args.dry_run:
        return {
            "success": True,
            "dry_run": True,
            "chain": "solana",
            "network": network,
            "rpc_url": rpc_url,
            "project_type": "anchor" if is_anchor else "native",
            "command": " ".join(cmd),
            "message": "Dry run — command generated but not executed.",
        }

    # Check tool availability (only for actual deployment)
    if is_anchor:
        if not _which("anchor"):
            return {
                "success": False,
                "error": "tool_not_found",
                "message": "anchor CLI is not installed",
                "install_hint": "cargo install --git https://github.com/coral-xyz/anchor avm && avm install latest && avm use latest",
            }
    else:
        if not _which("solana"):
            return {
                "success": False,
                "error": "tool_not_found",
                "message": "solana CLI is not installed",
                "install_hint": "sh -c \"$(curl -sSfL https://release.anza.xyz/stable/install)\"",
            }

    # For native, find the compiled .so file
    if not is_anchor:
        from pathlib import Path as _Path
        so_files = list(_Path(args.path).rglob("*.so"))
        if so_files:
            # Replace placeholder in cmd
            cmd[3] = str(so_files[0])
        else:
            return {
                "success": False,
                "error": "no_binary",
                "message": "No compiled .so file found. Run build first.",
            }

    # Execute
    try:
        r = _run(cmd, cwd=args.path, timeout=600)
        output = (r.stdout or "") + "\n" + (r.stderr or "")

        if r.returncode == 0:
            import re
            # Extract program ID from output
            program_id = args.program_id or "unknown"
            pid_match = re.search(r"Program Id:\s*([A-Za-z0-9]+)", output)
            if pid_match:
                program_id = pid_match.group(1)

            # Extract signature
            sig_match = re.search(r"Signature:\s*([A-Za-z0-9]+)", output)
            signature = sig_match.group(1) if sig_match else "unknown"

            explorer = net_config.get("explorer", "") if net_config else ""
            cluster_param = f"?cluster={network}" if network != "mainnet-beta" else ""

            return {
                "success": True,
                "chain": "solana",
                "network": network,
                "project_type": "anchor" if is_anchor else "native",
                "program_id": program_id,
                "signature": signature,
                "explorer_url": f"{explorer}/address/{program_id}{cluster_param}" if explorer else "",
                "tx_explorer_url": f"{explorer}/tx/{signature}{cluster_param}" if explorer and signature != "unknown" else "",
                "raw_output": output.strip()[:2000],
            }
        else:
            return {
                "success": False,
                "chain": "solana",
                "network": network,
                "error": "deployment_failed",
                "message": output.strip()[:2000],
                "command": " ".join(cmd),
            }
    except subprocess.TimeoutExpired:
        return {"success": False, "error": "timeout", "message": "Deployment timed out after 600s"}
    except Exception as exc:
        return {"success": False, "error": "execution_failed", "message": str(exc)}


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Blockchain contract deployment helper")
    parser.add_argument("--chain", required=True, choices=["solidity", "sui_move", "solana"],
                        help="Blockchain type")
    parser.add_argument("--path", required=True, help="Path to project root")
    parser.add_argument("--network", help="Target network name")
    parser.add_argument("--rpc-url", help="Custom RPC endpoint URL")
    parser.add_argument("--gas-budget", help="Gas budget / gas limit")
    parser.add_argument("--args", help="Constructor / init arguments (space-separated)")
    parser.add_argument("--contract", help="Specific contract to deploy (Solidity: src/X.sol:ContractName)")
    parser.add_argument("--verify", action="store_true", help="Verify contract on explorer (Solidity)")
    parser.add_argument("--dry-run", action="store_true", help="Generate command without executing")
    parser.add_argument("--private-key-env", help="Env var name containing private key (Solidity)")
    parser.add_argument("--keypair", help="Path to keypair file (Solana)")
    parser.add_argument("--program-id", help="Program ID to deploy to (Solana)")
    parser.add_argument("--skip-dependency-verification", action="store_true",
                        help="Skip dependency verification (Sui Move)")
    parser.add_argument("--list-networks", action="store_true",
                        help="List supported networks for the specified chain")

    args = parser.parse_args()

    if args.list_networks:
        networks = {
            "solidity": list(SOLIDITY_NETWORKS.keys()),
            "sui_move": list(SUI_NETWORKS.keys()),
            "solana": list(SOLANA_NETWORKS.keys()),
        }
        print(json.dumps(networks.get(args.chain, []), indent=2))
        return

    project_path = os.path.abspath(args.path)
    if not os.path.isdir(project_path):
        print(json.dumps({
            "success": False,
            "error": "invalid_path",
            "message": f"Project path does not exist: {project_path}",
        }))
        sys.exit(1)

    args.path = project_path

    # Mainnet safety check
    if args.network and _is_mainnet(args.network):
        print(json.dumps({
            "warning": "mainnet_deployment",
            "network": args.network,
            "message": "⚠️ You are about to deploy to MAINNET. This will cost real funds. "
                       "The AI agent should confirm this with the user before proceeding.",
        }), file=sys.stderr)

    # Dispatch
    deployers = {
        "solidity": deploy_solidity,
        "sui_move": deploy_sui_move,
        "solana": deploy_solana,
    }

    result = deployers[args.chain](args)
    result["timestamp"] = datetime.now(timezone.utc).isoformat()

    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
