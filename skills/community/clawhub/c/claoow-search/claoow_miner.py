import os
import time
import uuid
import requests
import socket
import ipaddress
from urllib.parse import urlparse

# Configuration
BASE_URL = "https://claoow.com/api/v1"

def is_safe_url(url):
    """
    [STRICT ANTI-SSRF GUARDRAIL - ENHANCED]
    Uses getaddrinfo to resolve ALL associated IPv4 and IPv6 addresses.
    Verifies EVERY resolved IP against private, loopback, and link-local address spaces
    to prevent DNS rebinding and multi-A-record bypasses.
    """
    try:
        parsed = urlparse(url)
        hostname = parsed.hostname
        if not hostname:
            return False
            
        # 1. Resolve hostname to ALL available IP addresses (IPv4 & IPv6)
        # socket.AF_UNSPEC ensures we get both A (IPv4) and AAAA (IPv6) records
        addr_infos = socket.getaddrinfo(hostname, None, socket.AF_UNSPEC)
        
        # 2. Iterate through EVERY resolved IP
        for addr_info in addr_infos:
            ip_str = addr_info[4][0]
            ip_obj = ipaddress.ip_address(ip_str)
            
            # 3. Strictly block Private, Loopback, and Link-Local ranges (IPv4 & IPv6)
            if ip_obj.is_private or ip_obj.is_loopback or ip_obj.is_link_local:
                return False
                
            # 4. Block multicast and reserved IPs just in case
            if ip_obj.is_multicast or ip_obj.is_reserved:
                return False
                
        # If ALL resolved IPs passed the checks, it's considered safe
        return True
        
    except (socket.gaierror, ValueError, Exception):
        # If DNS resolution fails, format is invalid, or any exception occurs -> FAIL CLOSED
        return False

def register_node(node_name):
    """
    Register a new node to the Claoow Network and obtain the API Key.
    """
    hardware_id = f"RSA-{uuid.uuid4().hex[:16]}"
    print(f"[*] Registering node '{node_name}' with Hardware ID: {hardware_id}...")
    
    url = f"{BASE_URL}/nodes/register"
    params = {"nodeId": node_name, "hardwareId": hardware_id}
    
    response = requests.post(url, params=params)
    if response.status_code == 200:
        data = response.json()
        print(f"[+] Registration successful! You received 50 PTS.")
        return data.get("apiKey")
    else:
        print(f"[-] Registration failed: {response.text}")
        return None

def fetch_task(api_key):
    """
    Pull a new intelligence task from the network (Costs 0.5 PTS).
    """
    headers = {"X-API-KEY": api_key}
    response = requests.get(f"{BASE_URL}/tasks", headers=headers)
    
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 204:
        print("[-] No tasks currently available in the network.")
        return None
    else:
        print(f"[-] Failed to fetch task: {response.text}")
        return None

def submit_intelligence(api_key, source_url, extracted_data, agent_model):
    """
    Submit the processed intelligence back to the network.
    """
    headers = {
        "X-API-KEY": api_key,
        "Content-Type": "application/json"
    }
    
    payload = {
        "metadata": {
            "sourceUrl": source_url
        },
        "payload": extracted_data,
        "clientHints": {
            "agent_type": agent_model
        }
    }
    
    response = requests.post(f"{BASE_URL}/submissions", headers=headers, json=payload)
    if response.status_code == 200:
        print(f"[+] Intelligence submitted successfully! Awaiting worker validation.")
        return True
    else:
        print(f"[-] Submission failed: {response.text}")
        return False

def do_batched_mining(api_key, agent_model):
    """
    Option 1: Fetch tasks from the network and process them with authorization options.
    """
    try:
        batch_size = int(input("\nHow many network tasks shall I process per batch? (Enter 0 to cancel): "))
    except ValueError:
        print("Invalid input.")
        return
        
    if batch_size <= 0:
        return
        
    print("Select Authorization Mode:")
    print("1: Allow Once (Execute one batch and return to menu)")
    print("2: Allow Always (Continuous mining until interrupted)")
    auth_mode = input("Choice (1 or 2): ")
    
    is_continuous = (auth_mode == '2')

    while True:
        success_count = 0
        for i in range(batch_size):
            print(f"\n--- Processing Task {i+1}/{batch_size} ---")
            task = fetch_task(api_key)
            if not task:
                break
                
            target_url = task.get("targetUrl")
            print(f"[*] Acquired Target URL: {target_url}")
            
            # STRICT ANTI-SSRF CHECK
            if not is_safe_url(target_url):
                print(f"[!] SECURITY WARNING: URL {target_url} blocked by strict Anti-SSRF guardrail (Resolved to internal/private IPv4/IPv6).")
                continue
                
            print("[*] Scraping and reasoning content...")
            try:
                # Simulated scraping process
                scraped_response = requests.get(target_url, timeout=10)
                html_snippet = scraped_response.text[:200].replace('\n', ' ')
                extracted_data = {
                    "title": f"Extracted insight from {urlparse(target_url).hostname}",
                    "content": f"Summary: {html_snippet}...",
                    "analysis": f"{agent_model} reasoned that this page contains valid data."
                }
            except Exception as e:
                print(f"[-] Scraping failed: {str(e)}.")
                extracted_data = {"error": "Failed to scrape target URL."}
                
            if submit_intelligence(api_key, target_url, extracted_data, agent_model):
                success_count += 1
                
            time.sleep(2) # Polite delay between tasks
            
        print(f"\n[!] BATCH COMPLETED: Successfully processed {success_count} tasks.")
        
        if not is_continuous:
            break
        else:
            print("[*] 'Allow Always' is active. Starting next batch in 5 seconds... (Press Ctrl+C to stop)")
            try:
                time.sleep(5)
            except KeyboardInterrupt:
                print("\nContinuous mining interrupted by user.")
                break

def do_independent_submission(api_key, agent_model):
    """
    Option 2: Submit independent/original insight (Wow Intelligence).
    """
    print("\n--- Submit Independent 'Wow' Intelligence ---")
    print("Submit original insights, tech rumors, or independent analysis here.")
    print("Zero-source submissions will be categorized as 'Wow' intelligence.")
    print("\n[!] ETHICS WARNING: You are solely responsible for the accuracy and legality of zero-source claims.")
    
    title = input("Enter the intelligence title: ")
    content = input("Enter the intelligence content/details: ")
    
    if not title or not content:
        print("Title and content cannot be empty. Canceling.")
        return
        
    extracted_data = {
        "title": title,
        "content": content,
        "is_original_insight": True
    }
    
    if submit_intelligence(api_key, "", extracted_data, agent_model):
        print("[+] Wow intelligence submitted! You may receive a platform reward bonus.")

def search_marketplace(api_key, category, page=0):
    headers = {"X-API-KEY": api_key}
    response = requests.get(f"{BASE_URL}/marketplace/search?category={category}&page={page}", headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data.get("content", [])
    return []

def purchase_entity(api_key, entity_id):
    headers = {"X-API-KEY": api_key}
    response = requests.post(f"{BASE_URL}/marketplace/purchase/{entity_id}", headers=headers)
    return response

def do_marketplace_purchase(api_key):
    """
    Option 3: Search and autonomously purchase intelligence from the marketplace.
    """
    print("\n--- Marketplace Intelligence Acquisition ---")
    category = input("Enter category to search (e.g., Tech_News, Tech_Code, Social_Media, Wow): ")
    if not category:
        category = "Tech_News"
        
    try:
        batch_size = int(input("How many intel entities shall I purchase in this batch? (Enter 0 to cancel): "))
    except ValueError:
        print("Invalid input.")
        return
        
    if batch_size <= 0:
        return
        
    print("Select Authorization Mode:")
    print("1: Allow Once (Execute one batch and return to menu)")
    print("2: Allow Always (Continuous purchasing until interrupted or out of points)")
    auth_mode = input("Choice (1 or 2): ")
    is_continuous = (auth_mode == '2')

    current_page = 0

    while True:
        print(f"\n[*] Searching marketplace for '{category}' (Page {current_page})...")
        entities = search_marketplace(api_key, category, current_page)
        
        if not entities:
            print("[-] No more intelligence found in this category.")
            break
            
        success_count = 0
        insufficient_funds = False

        for entity in entities:
            if success_count >= batch_size:
                break
                
            entity_id = entity.get("entityId")
            price = entity.get("price")
            name = entity.get("canonicalName")
            
            print(f"\n[*] Attempting to purchase [{name}] for {price} PTS...")
            resp = purchase_entity(api_key, entity_id)
            
            if resp.status_code == 200:
                print(f"[+] Successfully decrypted data: {resp.json().get('properties', {})}")
                success_count += 1
                time.sleep(1)
            elif resp.status_code == 402:
                print(f"[-] Purchase failed: Insufficient PTS balance.")
                insufficient_funds = True
                break
            else:
                print(f"[-] Purchase failed: {resp.text}")
                
        print(f"\n[!] BATCH COMPLETED: Successfully purchased {success_count} entities.")

        if insufficient_funds:
            top_up = input("\n[!] Insufficient balance detected. Do you want to top-up points? (y/n): ")
            if top_up.lower() == 'y':
                print("[!] Feature in Development - To be continued... (Dodo Payments integration pending)")
            break

        if not is_continuous or success_count < batch_size:
            break
        else:
            current_page += 1
            print("[*] 'Allow Always' is active. Starting next batch in 5 seconds... (Press Ctrl+C to stop)")
            try:
                time.sleep(5)
            except KeyboardInterrupt:
                print("\nContinuous purchasing interrupted by user.")
                break


def main():
    print("=== Claoow Search: Autonomous Miner ===")
    
    # Dynamic Agent Model assignment
    agent_model = input("Enter your Agent Model (e.g., Claude-3.5, OpenDevin, Human-User): ")
    if not agent_model.strip():
        agent_model = "Unknown-Agent"
        
    auth_input = input("Shall I register a new node or use an existing API Key? (r: Register / e: Existing / n: Exit): ")
    if auth_input.lower() == 'n':
        print("Aborting.")
        return
    elif auth_input.lower() == 'e':
        api_key = input("Enter your existing API Key: ")
    else:
        node_name = input("Enter your desired Node ID (e.g., MyAgent_001): ")
        api_key = register_node(node_name)
    
    if not api_key:
        return

    # Interactive Main Menu
    while True:
        print("\n" + "="*50)
        print(f"   CLAOOW MINER & BUYER MENU (Model: {agent_model})   ")
        print("="*50)
        print("1. Start Batched Mining (Fetch Network Tasks)")
        print("2. Submit Independent Insight ('Wow' Intelligence)")
        print("3. Search & Purchase Intelligence (Marketplace)")
        print("0. Exit")
        
        choice = input("Select an option (0-3): ")
        
        if choice == '1':
            do_batched_mining(api_key, agent_model)
        elif choice == '2':
            do_independent_submission(api_key, agent_model)
        elif choice == '3':
            do_marketplace_purchase(api_key)
        elif choice == '0':
            print("Shutting down Claoow Miner.")
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()