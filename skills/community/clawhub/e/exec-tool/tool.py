import subprocess

def exec_command(command: str) -> str:
    """
    Execute a safe shell command and return output
    """

    # 🔒 Basic safety restriction (VERY IMPORTANT)
    allowed_commands = ["clawhub"]

    if not any(command.startswith(cmd) for cmd in allowed_commands):
        return "Command not allowed"

    try:
        result = subprocess.getoutput(command)
        return result[:4000]  # Telegram limit safe
    except Exception as e:
        return str(e)
