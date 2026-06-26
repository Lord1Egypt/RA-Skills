#!/usr/bin/env python3
"""
claw-auth_cli - MFA-bound Secret Protection Tool

Provides TOTP-based encryption for sensitive data, requiring MFA code for decryption.

Multi-tenant support:
- System level: ~/.authlock/
- Workspace level: <WORKSPACE>/.authlock/
- User level: Custom path

Lookup priority: User → Workspace → System
"""

import argparse
import base64
import json
import os
import sys
import getpass
from datetime import datetime
from pathlib import Path
from typing import Optional

try:
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    import pyotp
    import qrcode
except ImportError as e:
    print(f"Error: Missing dependency - {e}")
    print("Install: pip install cryptography pyotp qrcode")
    sys.exit(1)


# Configuration
SYSTEM_HOME = Path.home() / ".authlock"
CONFIG_FILE = "config.json"
SEALED_DIR = "sealed"

# Workspace path (can be set via env var or parameter)
WORKSPACE_ENV = "OPENCLAW_WORKSPACE"


def get_workspace() -> Optional[Path]:
    """Get workspace path"""
    workspace = os.environ.get(WORKSPACE_ENV)
    if workspace:
        return Path(workspace)
    # Try common workspace locations
    common_paths = [
        Path.home() / ".openclaw" / "workspace",
        Path.cwd(),
    ]
    for p in common_paths:
        if p.exists() and (p / ".authlock").exists():
            return p
    return None


def find_authlock_home(user_path: Optional[str] = None) -> Path:
    """
    Find authlock location by priority
    
    Priority: User → Workspace → System
    """
    # 1. User level: specified via parameter or env var
    if user_path:
        return Path(user_path)
    
    env_home = os.environ.get("AUTHLOCK_HOME")
    if env_home:
        return Path(env_home)
    
    # 2. Workspace level
    workspace = get_workspace()
    if workspace:
        workspace_home = workspace / ".authlock"
        if workspace_home.exists():
            return workspace_home
    
    # 3. System level (default)
    return SYSTEM_HOME


def get_home(args_path: Optional[str] = None) -> Path:
    """Get current authlock home directory"""
    return find_authlock_home(args_path)


def ensure_home(home: Path):
    """Ensure directory exists"""
    home.mkdir(parents=True, exist_ok=True)
    (home / SEALED_DIR).mkdir(parents=True, exist_ok=True)


def load_config(home: Path) -> dict:
    """Load configuration"""
    config_path = home / CONFIG_FILE
    if config_path.exists():
        with open(config_path, "r") as f:
            return json.load(f)
    return {}


def save_config(home: Path, config: dict):
    """Save configuration"""
    config_path = home / CONFIG_FILE
    with open(config_path, "w") as f:
        json.dump(config, f, indent=2)


def derive_key(seed: str, salt: bytes, pin: Optional[str] = None) -> bytes:
    """Derive encryption key from TOTP seed"""
    password = seed.encode()
    if pin:
        password = (seed + pin).encode()
    
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    return kdf.derive(password)


def encrypt_data(data: bytes, seed: str, pin: Optional[str] = None) -> dict:
    """Encrypt data"""
    import secrets
    
    salt = secrets.token_bytes(16)
    key = derive_key(seed, salt, pin)
    
    aesgcm = AESGCM(key)
    iv = secrets.token_bytes(12)
    
    ciphertext = aesgcm.encrypt(iv, data, None)
    
    return {
        "version": 1,
        "algorithm": "AES-256-GCM",
        "kdf": "PBKDF2-SHA256",
        "kdf_iterations": 100000,
        "salt": base64.b64encode(salt).decode(),
        "iv": base64.b64encode(iv).decode(),
        "ciphertext": base64.b64encode(ciphertext).decode(),
        "created_at": datetime.utcnow().isoformat() + "Z",
    }


def decrypt_data(sealed: dict, seed: str, pin: Optional[str] = None) -> bytes:
    """Decrypt data"""
    salt = base64.b64decode(sealed["salt"])
    iv = base64.b64decode(sealed["iv"])
    ciphertext = base64.b64decode(sealed["ciphertext"])
    
    key = derive_key(seed, salt, pin)
    aesgcm = AESGCM(key)
    
    try:
        return aesgcm.decrypt(iv, ciphertext, None)
    except Exception as e:
        raise ValueError(f"Decryption failed: {e}")


def generate_qrcode(uri: str):
    """Display QR code in terminal"""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=2,
    )
    qr.add_data(uri)
    qr.make(fit=True)
    qr.print_ascii(invert=True)


def get_level_name(home: Path) -> str:
    """Get location level name"""
    if home == SYSTEM_HOME:
        return "系统级"
    
    workspace = get_workspace()
    if workspace and home == workspace / ".authlock":
        return "工作区级"
    
    return "用户级"


def prompt_init_level() -> tuple[str, Optional[Path]]:
    """Interactively prompt for initialization level"""
    print("\n请选择初始化级别:")
    print("  1. 系统级 (~/.authlock/) - 所有工作区共享")
    print("  2. 工作区级 (<WORKSPACE>/.authlock/) - 当前工作区独立")
    print("  3. 用户级 - 自定义路径")
    
    workspace = get_workspace()
    if workspace:
        print(f"\n当前工作区: {workspace}")
    
    choice = input("\n选择 (1/2/3): ").strip()
    
    if choice == "1":
        return "system", None
    elif choice == "2":
        if workspace:
            return "workspace", workspace / ".authlock"
        else:
            print("错误: 未检测到工作区，请使用系统级或用户级")
            return None, None
    elif choice == "3":
        custom_path = input("输入自定义路径: ").strip()
        if custom_path:
            return "user", Path(custom_path)
        else:
            print("错误: 路径不能为空")
            return None, None
    else:
        print("错误: 无效选择")
        return None, None


def cmd_init(args):
    """Initialize authlock"""
    # 确定初始化位置
    if args.level:
        if args.level == "system":
            home = SYSTEM_HOME
        elif args.level == "workspace":
            workspace = get_workspace()
            if not workspace:
                print("错误: 未检测到工作区，请设置 OPENCLAW_WORKSPACE 环境变量")
                return
            home = workspace / ".authlock"
        elif args.level == "user":
            if not args.path:
                print("错误: 用户级需要 --path 参数")
                return
            home = Path(args.path)
        else:
            print(f"错误: 无效级别 '{args.level}'，可选: system, workspace, user")
            return
    elif args.path:
        home = Path(args.path)
    else:
        # 交互式选择
        level, home = prompt_init_level()
        if not home:
            return
    
    ensure_home(home)
    config = load_config(home)
    
    if "totp_seed" in config:
        level_name = get_level_name(home)
        print(f"Warning: TOTP config already exists at {level_name}, re-init will overwrite")
        print(f"Location: {home}")
        response = input("Continue? (y/N): ")
        if response.lower() != "y":
            print("Cancelled")
            return
    
    if args.seed:
        seed = args.seed.upper().replace(" ", "")
        if not seed:
            print("Error: Seed cannot be empty")
            return
    else:
        seed = pyotp.random_base32()
    
    # Create TOTP object
    totp = pyotp.TOTP(seed)
    
    # Generate URI for QR code
    issuer = "authlock"
    account = os.environ.get("USER", "user")
    
    # Set account name suffix based on location
    level_name = get_level_name(home)
    if level_name != "system":
        account = f"{account}@{home.parent.name}"
    
    uri = totp.provisioning_uri(name=account, issuer_name=issuer)
    
    # Display seed and QR code
    print(f"\nInit location: {home} ({level_name})")
    print(f"\nTOTP seed: {seed}")
    print(f"\nScan QR code with Microsoft Authenticator:\n")
    generate_qrcode(uri)
    
    print(f"\nOr add manually - Account: {account}, Seed: {seed}")
    
    # Verify
    print("\nEnter 6-digit code from Authenticator to confirm:")
    code = input("Code: ").strip()
    
    if totp.verify(code, valid_window=1):
        config["totp_seed"] = seed
        config["created_at"] = datetime.utcnow().isoformat() + "Z"
        config["level"] = level_name
        save_config(home, config)
        print(f"\n✅ Initialized successfully!")
        print(f"   Location: {home}")
    else:
        print("\n❌ Code incorrect, init cancelled")
        print("Ensure system time is accurate")


def cmd_seal(args):
    """Seal (encrypt) a secret"""
    home = get_home(args.path)
    
    if not home.exists():
        print(f"Error: Location not found - {home}")
        print("Run 'authlock init' first")
        return
    
    ensure_home(home)
    config = load_config(home)
    
    if "totp_seed" not in config:
        print(f"Error: {home} not initialized")
        print("Run 'authlock init' first")
        return
    
    # 确定名称
    name = args.name or Path(args.file).stem
    
    # 读取数据
    if args.file == "-":
        data = sys.stdin.buffer.read()
    else:
        file_path = Path(args.file)
        if not file_path.exists():
            print(f"错误: 文件不存在 - {file_path}")
            return
        with open(file_path, "rb") as f:
            data = f.read()
    
    # 可选 PIN
    pin = None
    if args.pin or (config.get("require_pin") and not args.no_pin):
        pin = getpass.getpass("输入 PIN: ")
    
    # 加密
    sealed = encrypt_data(data, config["totp_seed"], pin)
    sealed["name"] = name
    sealed["type"] = "binary" if args.file != "-" else "text"
    
    # 保存
    sealed_path = home / SEALED_DIR / f"{name}.sealed"
    with open(sealed_path, "w") as f:
        json.dump(sealed, f, indent=2)
    
    level_name = get_level_name(home)
    print(f"✅ 已封印: {name}")
    print(f"   位置: {home} ({level_name})")


def cmd_open(args):
    """Open (decrypt) a secret"""
    home = get_home(args.path)
    
    if not home.exists():
        print(f"错误: 位置不存在 - {home}")
        return
    
    config = load_config(home)
    
    if "totp_seed" not in config:
        print(f"错误: {home} 未初始化")
        return
    
    # 查找封印文件
    sealed_path = home / SEALED_DIR / f"{args.name}.sealed"
    if not sealed_path.exists():
        print(f"错误: 找不到封印 - {args.name}")
        print(f"位置: {home}")
        return
    
    # 加载封印数据
    with open(sealed_path, "r") as f:
        sealed = json.load(f)
    
    # 验证 TOTP
    if not args.code:
        args.code = input("输入 TOTP 验证码: ").strip()
    
    totp = pyotp.TOTP(config["totp_seed"])
    if not totp.verify(args.code, valid_window=1):
        print("❌ 验证码不正确")
        return
    
    # 可选 PIN
    pin = None
    if args.pin or config.get("require_pin"):
        pin = getpass.getpass("输入 PIN (如无 PIN 直接回车): ")
        if not pin:
            pin = None
    
    # 解密
    try:
        data = decrypt_data(sealed, config["totp_seed"], pin)
    except ValueError as e:
        print(f"❌ {e}")
        print("提示: 如果设置了 PIN，请确保输入正确的 PIN")
        return
    
    # 输出
    if args.output:
        output_path = Path(args.output)
        with open(output_path, "wb") as f:
            f.write(data)
        if sealed.get("type") == "binary":
            os.chmod(output_path, 0o600)
        print(f"✅ 已解密到: {output_path}")
    elif args.exec:
        import subprocess
        import tempfile
        with tempfile.NamedTemporaryFile(mode="wb", delete=False, suffix=".tmp") as tmp:
            tmp.write(data)
            tmp_path = tmp.name
        try:
            os.chmod(tmp_path, 0o600)
            cmd = args.exec.replace("-", tmp_path)
            subprocess.run(cmd, shell=True)
        finally:
            os.unlink(tmp_path)
    else:
        if sealed.get("type") == "text":
            sys.stdout.write(data.decode("utf-8"))
        else:
            sys.stdout.buffer.write(data)


def cmd_list(args):
    """List all sealed secrets"""
    home = get_home(args.path)
    
    if not home.exists():
        print(f"位置不存在: {home}")
        return
    
    sealed_dir = home / SEALED_DIR
    
    if not sealed_dir.exists():
        print(f"位置: {home}")
        print("没有封印的机密")
        return
    
    sealed_files = list(sealed_dir.glob("*.sealed"))
    
    level_name = get_level_name(home)
    print(f"位置: {home} ({level_name})")
    
    if not sealed_files:
        print("没有封印的机密")
        return
    
    print(f"封印的机密 ({len(sealed_files)} 个):\n")
    for path in sorted(sealed_files):
        with open(path, "r") as f:
            sealed = json.load(f)
        
        created = sealed.get("created_at", "unknown")
        type_ = sealed.get("type", "unknown")
        
        print(f"  • {sealed.get('name', path.stem)}")
        print(f"    类型: {type_}")
        print(f"    创建: {created}")
        print()


def cmd_delete(args):
    """Delete a secret"""
    home = get_home(args.path)
    
    if not home.exists():
        print(f"错误: 位置不存在 - {home}")
        return
    
    sealed_path = home / SEALED_DIR / f"{args.name}.sealed"
    
    if not sealed_path.exists():
        print(f"错误: 找不到封印 - {args.name}")
        print(f"位置: {home}")
        return
    
    if not args.yes:
        response = input(f"确认删除 {args.name}? (y/N): ")
        if response.lower() != "y":
            print("已取消")
            return
    
    sealed_path.unlink()
    print(f"✅ 已删除: {args.name}")


def cmd_config(args):
    """Configuration management"""
    home = get_home(args.path)
    
    if not home.exists():
        print(f"错误: 位置不存在 - {home}")
        return
    
    ensure_home(home)
    config = load_config(home)
    
    if args.set_pin:
        pin = getpass.getpass("设置新 PIN: ")
        pin_confirm = getpass.getpass("确认 PIN: ")
        if pin != pin_confirm:
            print("错误: PIN 不匹配")
            return
        if pin:
            config["pin_hash"] = base64.b64encode(pin.encode()).decode()
            print("✅ PIN 已设置")
        else:
            config.pop("pin_hash", None)
            print("✅ PIN 已清除")
        save_config(home, config)
    
    elif args.require_pin:
        config["require_pin"] = True
        save_config(home, config)
        print("✅ 已启用强制 PIN")
    
    elif args.no_require_pin:
        config["require_pin"] = False
        save_config(home, config)
        print("✅ 已禁用强制 PIN")


def cmd_which(args):
    """Show current location being used"""
    home = get_home(args.path)
    level_name = get_level_name(home)
    
    print(f"当前位置: {home}")
    print(f"级别: {level_name}")
    
    # 显示查找路径
    print("\n查找优先级:")
    
    # 用户级（环境变量）
    env_home = os.environ.get("CLAWAUTH_HOME")
    if env_home:
        print(f"  1. 用户级 (CLAWAUTH_HOME): {env_home} ✓")
    elif args.path:
        print(f"  1. 用户级 (--path): {args.path} ✓")
    else:
        print(f"  1. 用户级: 未指定")
    
    # 工作区级
    workspace = get_workspace()
    if workspace:
        ws_home = workspace / ".authlock"
        status = "✓" if ws_home.exists() and home == ws_home else "○"
        print(f"  2. 工作区级: {ws_home} {status}")
    else:
        print(f"  2. 工作区级: 未检测到")
    
    # 系统级
    status = "✓" if home == SYSTEM_HOME else "○"
    print(f"  3. 系统级: {SYSTEM_HOME} {status}")
    
    # 显示配置状态
    if home.exists():
        config = load_config(home)
        if "totp_seed" in config:
            created = config.get("created_at", "unknown")
            print(f"\n已初始化: {created}")
            
            sealed_dir = home / SEALED_DIR
            if sealed_dir.exists():
                count = len(list(sealed_dir.glob("*.sealed")))
                print(f"封印数量: {count}")
        else:
            print("\n未初始化")


def cmd_locations(args):
    """List all.authlock locations"""
    print("所有.authlock 位置:\n")
    
    locations = []
    
    # 系统级
    if SYSTEM_HOME.exists():
        config = load_config(SYSTEM_HOME)
        has_seed = "totp_seed" in config
        locations.append(("系统级", SYSTEM_HOME, has_seed))
    
    # 工作区级
    workspace = get_workspace()
    if workspace:
        ws_home = workspace / ".authlock"
        if ws_home.exists():
            config = load_config(ws_home)
            has_seed = "totp_seed" in config
            locations.append(("工作区级", ws_home, has_seed))
    
    # 搜索其他工作区
    common_paths = [
        Path.home() / ".openclaw" / "workspace",
        Path.cwd(),
    ]
    for p in common_paths:
        ws_home = p / ".authlock"
        if ws_home.exists() and ws_home not in [loc[1] for loc in locations]:
            config = load_config(ws_home)
            has_seed = "totp_seed" in config
            locations.append((f"工作区级 ({p.name})", ws_home, has_seed))
    
    # 用户级（环境变量）
    env_home = os.environ.get("CLAWAUTH_HOME")
    if env_home:
        env_path = Path(env_home)
        if env_path.exists():
            config = load_config(env_path)
            has_seed = "totp_seed" in config
            locations.append(("用户级 (CLAWAUTH_HOME)", env_path, has_seed))
    
    if not locations:
        print("未找到任何.authlock 位置")
        print("请先运行 .authlock init' 初始化")
        return
    
    for level, path, has_seed in locations:
        status = "✓ 已初始化" if has_seed else "○ 未初始化"
        sealed_dir = path / SEALED_DIR
        count = len(list(sealed_dir.glob("*.sealed"))) if sealed_dir.exists() else 0
        print(f"  [{level}]")
        print(f"    路径: {path}")
        print(f"    状态: {status}")
        print(f"    封印: {count} 个")
        print()


def main():
    parser = argparse.ArgumentParser(
        description="claw-auth - MFA-bound Secret Protection Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Multi-tenant support:
  System      ~/.authlock/           Shared across all workspaces
  Workspace   <WORKSPACE>/.authlock/ Independent for current workspace
  User        Custom path            User-specified location

Lookup priority: User (--path/CLAWAUTH_HOME) → Workspace → System

Examples:
  claw-auth init                     # Interactive level selection
  claw-auth init --level system      # System level
  claw-auth init --level workspace   # Workspace level
  claw-auth init --level user --path /custom/path  # User level
  claw-auth which                    # Show current location
  claw-auth locations                # List all locations
        """
    )
    parser.add_argument("--path", "-p", help="指定.authlock 位置 (用户级)")
    
    subparsers = parser.add_subparsers(dest="command", help="命令")

    # init
    init_parser = subparsers.add_parser("init", help="初始化 TOTP 配置")
    init_parser.add_argument("--level", "-l", 
                             choices=["system", "workspace", "user"],
                             help="初始化级别: system, workspace, user")
    init_parser.add_argument("--seed", "-s", help="导入现有 TOTP 种子 (base32)")
    init_parser.set_defaults(func=cmd_init)

    # seal
    seal_parser = subparsers.add_parser("seal", help="加密封印机密")
    seal_parser.add_argument("file", help="要加密的文件路径 (使用 - 从 stdin 读取)")
    seal_parser.add_argument("--name", "-n", help="机密名称 (默认: 文件名)")
    seal_parser.add_argument("--pin", action="store_true", help="使用 PIN 保护")
    seal_parser.add_argument("--no-pin", action="store_true", help="跳过 PIN")
    seal_parser.set_defaults(func=cmd_seal)

    # open
    open_parser = subparsers.add_parser("open", help="解密机密")
    open_parser.add_argument("name", help="机密名称")
    open_parser.add_argument("--code", "-c", help="TOTP 验证码")
    open_parser.add_argument("--output", "-o", help="输出文件路径")
    open_parser.add_argument("--exec", "-e", help="执行命令 (- 替换为解密文件)")
    open_parser.add_argument("--pin", action="store_true", help="使用 PIN")
    open_parser.set_defaults(func=cmd_open)

    # list
    list_parser = subparsers.add_parser("list", help="列出所有封印的机密")
    list_parser.set_defaults(func=cmd_list)

    # delete
    delete_parser = subparsers.add_parser("delete", help="删除机密")
    delete_parser.add_argument("name", help="机密名称")
    delete_parser.add_argument("--yes", "-y", action="store_true", help="跳过确认")
    delete_parser.set_defaults(func=cmd_delete)

    # config
    config_parser = subparsers.add_parser("config", help="配置管理")
    config_parser.add_argument("--set-pin", action="store_true", help="设置 PIN")
    config_parser.add_argument("--require-pin", action="store_true", help="启用强制 PIN")
    config_parser.add_argument("--no-require-pin", action="store_true", help="禁用强制 PIN")
    config_parser.set_defaults(func=cmd_config)

    # which
    which_parser = subparsers.add_parser("which", help="显示当前位置")
    which_parser.set_defaults(func=cmd_which)

    # locations
    locations_parser = subparsers.add_parser("locations", help="列出所有.authlock 位置")
    locations_parser.set_defaults(func=cmd_locations)

    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    args.func(args)


if __name__ == "__main__":
    main()