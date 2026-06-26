"""
fetch_graph.py - A lightweight script to interact with the TrustIn API and retrieve
the raw transaction graph data for a given blockchain address.

This script does NOT perform rule evaluation. It only fetches the data and saves it
to a JSON file for downstream LLM or system consumption.
"""
import os
import json
import argparse
from typing import Dict
from datetime import datetime

from trustin_api import TrustInAPI

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

def fetch_graph(chain: str, address: str, direction: str = "inflow", inflow_hops: int = 3, outflow_hops: int = 3, api_key: str = None, min_timestamp: int = None, max_timestamp: int = None, max_nodes_per_hop: int = 100) -> Dict:
    """Fetches graph data for an address using TrustInAPI."""
    start_time = datetime.now()
    
    # Apply defaults for timestamps (4 years ago and now) if not provided
    if not max_timestamp:
        max_timestamp = int(start_time.timestamp() * 1000)
    if not min_timestamp:
        four_years_ago = start_time.timestamp() - (4 * 365 * 24 * 60 * 60)
        min_timestamp = int(four_years_ago * 1000)
        
    try:
        api = TrustInAPI(api_key=api_key)
        # TrustIn API automatically uses async_detect underneath
        kwargs = {
            "inflow_hops": inflow_hops, 
            "outflow_hops": outflow_hops,
            "max_nodes_per_hop": max_nodes_per_hop,
            "min_timestamp": min_timestamp,
            "max_timestamp": max_timestamp
        }
        
        result = api.kya_pro_detect(chain, address, **kwargs)
        
        # Package the raw graph details returned by the API
        response = {
            "chain": chain,
            "address": address,
            "direction": direction,
            "hops_requested": {
                "inflow": inflow_hops,
                "outflow": outflow_hops
            },
            "parameters": {
                "max_nodes_per_hop": max_nodes_per_hop,
                "min_timestamp_ms": min_timestamp,
                "max_timestamp_ms": max_timestamp
            },
            "timestamp": datetime.now().isoformat(),
            "execution_time": str(datetime.now() - start_time),
            "graph_data": result.details # The raw parsed JSON graph
        }
        return response
        
    except Exception as e:
        print(f"[ERROR] Failed to fetch graph: {str(e)}")
        import traceback
        traceback.print_exc()
        return {}

def main():
    parser = argparse.ArgumentParser(description="Fetch TrustIn raw graph data.")
    parser.add_argument("chain", help="Blockchain network (e.g., Tron, Ethereum)")
    parser.add_argument("address", help="Wallet address to investigate")
    parser.add_argument("--direction", choices=["inflow", "outflow", "all"], default="inflow", help="Trace direction")
    parser.add_argument("--inflow-hops", type=int, default=3, help="Inflow depth (default: 3)")
    parser.add_argument("--outflow-hops", type=int, default=3, help="Outflow depth (default: 3)")
    parser.add_argument("--max-nodes", type=int, default=100, help="Max nodes per hop (default: 100, max: 1000)")
    parser.add_argument("--min-timestamp", type=int, help="Min timestamp in milliseconds (default: 4 years ago)")
    parser.add_argument("--max-timestamp", type=int, help="Max timestamp in milliseconds (default: now)")
    parser.add_argument("--api-key", help="TrustIn API Key (optional if in env)")
    
    args = parser.parse_args()
    
    print(f"📡 Fetching Graph for {args.chain} - {args.address}...")
    print(f"   Direction: {args.direction.upper()} | Inflow: {args.inflow_hops} hops | Outflow: {args.outflow_hops} hops | Max Nodes: {args.max_nodes}")
    
    result = fetch_graph(
        chain=args.chain,
        address=args.address,
        direction=args.direction,
        inflow_hops=args.inflow_hops,
        outflow_hops=args.outflow_hops,
        max_nodes_per_hop=args.max_nodes,
        api_key=args.api_key,
        min_timestamp=args.min_timestamp,
        max_timestamp=args.max_timestamp
    )
    
    if result and result.get("graph_data"):
        # Create directories in the current working directory
        reports_dir = os.path.join(os.getcwd(), "reports")
        graph_dir = os.path.join(os.getcwd(), "graph_data")
        os.makedirs(reports_dir, exist_ok=True)
        os.makedirs(graph_dir, exist_ok=True)
        
        timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        json_path = os.path.join(graph_dir, f"raw_graph_{args.address}_{timestamp_str}.json")
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
            
        print(f"\n✅ SUCCESS: Raw Graph JSON saved to: {json_path}")
        print(f"👉 Now hand over to the LLM Agent to evaluate against rules.json!")
    else:
        print("\n❌ FAILED: Could not retrieve graph data.")
        exit(1)

if __name__ == "__main__":
    main()
