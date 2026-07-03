---
name: celaut-bridge-skill
version: 1.1.0
description: Bridge skill to install Celaut Nodo via official script, pack services, execute decentralized microVM workloads, and discover Unstoppable Skills on-chain or via MCP.
author: Community Contribution
license: MIT
system_requirements:
  apps:
    - curl
    - git
    - sudo
    - iptables
    - bc
---

# Celaut Bridge Skill

This skill (formatted according to the [agentskills.io](https://agentskills.io/) specification) enables any AI agent to interface with the Celaut ecosystem. It provides automated context to install the Celaut Node (`nodo`), package project services (`.celaut` / `.csp`), execute deterministic decentralized workloads via microVMs, and discover **Unstoppable Skills** (Celaut Skills) either directly on-chain or through Model Context Protocol (MCP).

## 1. Celaut Node Installation & Management

The Celaut Node (`nodo`) orchestrates service execution across decentralized peer networks. It must be installed using the official automated installer on supported Debian/Ubuntu Linux distributions.

### Recommended Installation (Official Script)

Execute the following command to download and run the automated installer. Note that this requires `sudo` privileges to configure system routing (`iptables`) and virtualization runtimes:

```bash
curl --proto '=https' --tlsv1.2 -sSf https://raw.githubusercontent.com/celaut-project/nodo/stable/install.sh | sudo bash
```

### Alternative Installation (From Source & Development)

If direct script piping is restricted or you want a local source checkout (allowing code modifications to be tested by restarting the system service):

```bash
git clone https://github.com/celaut-project/nodo.git /home/user/nodo
cd /home/user/nodo
sudo ./install.sh --source-dir /home/user/nodo
```

To install from a specific branch (e.g., `dev`):

```bash
curl --proto '=https' --tlsv1.2 -sSf https://raw.githubusercontent.com/celaut-project/nodo/dev/install.sh | sudo bash -s -- --branch dev
```

For manual bootstrapping without executing `install.sh`, refer to the official [Manual Installation Guide](https://github.com/celaut-project/nodo/blob/master/docs/INSTALL.md).

---

## 2. Packaging Celaut Services (.csp / .celaut)

To deploy services on the Celaut Node, projects must be packaged into deterministic Celaut service specifications (`.celaut` / `.csp`) using the built-in packer command or retrieved from Unstoppable Skills registries.

> **Note on Containerization:** Docker is utilized **strictly for the packaging phase** (`nodo pack`) to build image layers and compile service specifications. Once packaged, services are executed using isolated **microVMs** (`ch`), completely separate from Docker container runtimes.

### Packer Workflow

The `nodo pack` command processes a local project directory containing a `Dockerfile` and configuration metadata to generate a standardized service specification package:

```bash
# Package a project directory into a Celaut service specification file
nodo pack /path/to/project
```

### Importing & Exporting Specifications

```bash
# Import an existing local service specification file
nodo import /path/to/service.celaut

# Export an installed service to disk
nodo export <service_id_or_tag> /export/path
```

### Feasibility & Cost Estimation

Before launching any workload, use `nodo estimate` to verify memory guard limits (`resources.at_most.mem_limit`), gas fees, and physical hardware availability (RAM, CPU cores, disk):

```bash
# Estimate execution feasibility and gas costs for a service specification file
nodo estimate ./my-service.celaut

# Estimate an installed service by hash ID or tag
nodo estimate 1234567890abcdef
nodo estimate my_service_tag
```

---

## 3. Service Execution & Runtime Management

When executing workloads, Celaut Nodo launches instances inside isolated microVMs (`ch`).

### Execution Lifecycle

1. **Inspection & Environment Declaration:**
   Before launching a service, inspect its architecture and declared environment variables. **The environment variables accepted during execution (`-e`) depend strictly on what the specific service declares.**
   ```bash
   # Inspect declared environment variables, resource boundaries, and metadata
   nodo inspect <service_id_or_tag>
   ```

2. **Launching Instances (`nodo execute`):**
   Execute a service by passing its hexadecimal hash ID or assigned tag. Runtime environment variables declared by the service are passed using `-e <key> <value>`. Use `--remote` to advertise host-facing network IPs.
   ```bash
   # Execute a basic service instance
   nodo execute 1234567890abcdef

   # Execute with declared environment variables and remote network advertisement
   nodo execute --remote -e workers 8 -e timeout 20 my_service_tag
   ```

3. **Instance Monitoring & Gas Control:**
   Use `nodo instances` to list active workloads. The output indicates which virtualizer is executing each instance (`ch`, `docker`, etc.), with the architectural standard being `ch` (Cloud Hypervisor microVMs).
   ```bash
   # List active running instances (shows instance ID, status, and virtualizer type)
   nodo instances

   # List running instances grouped by their parent service
   nodo instances --grouped

   # Dynamically adjust allocated gas for a running workload
   nodo increase_gas <instance_id> 100
   nodo decrease_gas <instance_id> 50

   # Terminate a running instance
   nodo kill <instance_id>

   # Remove a service specification from the local node registry
   nodo remove <service_id>
   ```

---

## 4. Unstoppable Skills (Celaut Skills) & MCP Integration

While the [agentskills.io](https://agentskills.io/) specification defines the structure of *this* bridge skill file (`SKILL.md`), **Unstoppable Skills** (Celaut Skills) represent the decentralized, 100% on-chain "problem store" for AI agents on the Celaut + Ergo blockchain ecosystem.

### Philosophy: Searching for Problems, Not Servers

In traditional architectures, agents look for centralized MCP servers or specific endpoints. In Celaut, **agents search for problems (Skills)** (e.g., `"Optimal XAU/BTC Performance"`, `"Sat-sorter"`). Each on-chain Skill entity automatically bundles:
* **Coverage:** Verifiable Celaut services that solve the problem (`celaut:coverage:v1`).
* **Benchmarks:** Deterministic specifications on how to measure performance (`celaut:benchmark:v1`).
* **Results:** Immutable comparative performance metrics submitted against benchmarks (`celaut:result:v1`).
* **Community Forum:** On-chain discussions and skin-in-the-game reputation validation.

Official Documentation: [Celaut Skills README](https://raw.githubusercontent.com/celaut-project/skills/refs/heads/main/README.md)

### Read-Only MCP Server Integration

Unstoppable Skills can also be seamlessly consumed via Model Context Protocol (MCP) using the official read-only MCP server. This allows any MCP client to query the on-chain registry without mutating state.

**Running the MCP Server:**
```bash
git clone https://github.com/celaut-project/skills.git
cd skills
npm install
npm run mcp
# Or execute directly over stdio: node mcp/server.mjs
```

**Available MCP Tools:**
* `load_skills`: Lists all registered problem capabilities (`celaut:skill:v1`).
* `load_coverages`: Lists deduplicated service IDs that directly or indirectly address a specific Skill box ID.
* `load_benchmarks`: Retrieves test specs, case descriptors, and metrics for a Skill.
* `load_results`: Retrieves comparative evaluation outputs submitted against a Benchmark.
* `load_skill_tree`: Convenience tool returning a complete nested tree of a Skill, its Coverages, Benchmarks, and Results in a single call.

Official Documentation: [Celaut Skills MCP Specification](https://raw.githubusercontent.com/celaut-project/skills/refs/heads/main/MCP.md)

---

## 5. Node Administration & Diagnostics

### Daemon Management (`systemd`)
When installed with superuser privileges, Nodo runs as a background system service (`nodo.service`).
```bash
# Check daemon service status
sudo nodo daemon status

# Start, stop, or restart the background service
sudo nodo daemon start | stop | restart

# Run comprehensive system diagnostics (virtualization flags, KVM access, guest kernel validation)
sudo nodo doctor

# Update Nodo to the latest release
sudo nodo update
```

### Basic Node Utilities
* `nodo services`: Lists all registered service packages on the local node.
* `nodo integrity --fix`: Verifies registry metadata integrity and repairs detected inconsistencies.
* `nodo tag <service_id> <alias>`: Assigns a human-readable alias tag to a hexadecimal service hash ID.
* `nodo peers` / `nodo clients`: Displays connected network nodes and clients.
* `nodo connect <ip:port>`: Manually initiates connection to a peer node.
* `nodo info`: Shows runtime versions, storage paths, and node identity.
* `nodo logs`: Displays real-time application daemon logs.

---

## 6. Agent Instructions & Rules

1. **Terminal-First CLI Execution:** Execute all interactions with Celaut via standard bash terminal commands.
2. **Idempotency Setup Check:** Prior to executing installation scripts, run `command -v nodo` to verify if the node binary is already available in PATH.
3. **Sudo Privileges Handling:** Automated installation and system daemon management (`daemon`, `doctor`, `update`) require root elevation. Ensure non-interactive execution (`sudo -n true`) is permitted or handle prompt elevation safely.
4. **Strict Environment Variable Declaration:** When preparing `nodo execute -e <key> <value>`, **never guess environment variables**. Always run `nodo inspect <service>` first to determine the exact environment variables declared and supported by the service package.
5. **MicroVM Execution Awareness:** Understand that services execute inside isolated microVMs (`ch`). Do not attempt to use Docker commands to inspect running service instances; Docker is strictly reserved for `nodo pack` layer compilation.
6. **Pre-flight Estimation:** Always run `nodo estimate <service>` before deploying unknown workloads to verify memory guard limits (`resources.at_most.mem_limit`) and ensure sufficient gas availability.
7. **Problem-First Discovery:** When seeking AI capabilities, query Unstoppable Skills (via `nodo` CLI or the MCP `load_skill_tree` tool) to evaluate comparative `Results` and verifiable `Coverage` before selecting a service ID.

---

## 7. References & Ecosystem Links

* [Celaut Nodo Repository](https://github.com/celaut-project/nodo)
* [Nodo User Guide (USAGE.md)](https://github.com/celaut-project/nodo/blob/master/docs/USAGE.md)
* [Manual Installation Guide (INSTALL.md)](https://github.com/celaut-project/nodo/blob/master/docs/INSTALL.md)
* [Know Your Assumptions (KyA.md)](https://github.com/celaut-project/nodo/blob/master/docs/KyA.md)
* [Ergo Blockchain Integration (ERGO.md)](https://github.com/celaut-project/nodo/blob/master/docs/ERGO.md)
* [Unstoppable Skills (Celaut Skills) README](https://raw.githubusercontent.com/celaut-project/skills/refs/heads/main/README.md)
* [Unstoppable Skills MCP Server Specification](https://raw.githubusercontent.com/celaut-project/skills/refs/heads/main/MCP.md)
* [Agent Skills Format Specification](https://agentskills.io/)
