# Thundarr Execution Bridge (Local)

The `exec_local` skill provides a direct interface for executing system-level shell commands within the `thundarr-gpu` container environment on Garuda. 

### Core Functionality
- **Direct Shell Access**: Allows for low-latency execution of binary tools and scripts.
- **Remote Orchestration**: Designed to be used as a jump-point for managing the Fedora UM250 host via the `thundarr-remote` SSH script.
- **Resource Monitoring**: Can be used to check local container health, process tables, and network availability between Docker nodes.

### Security Note
This tool executes commands with the permissions of the container user. Ensure all inputs are sanitized when used in automated workflows.
