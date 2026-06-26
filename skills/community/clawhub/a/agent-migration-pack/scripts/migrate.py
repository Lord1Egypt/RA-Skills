#!/usr/bin/env python3
"""
Agent 迁移包管理脚本
v1.0.5

功能：
- python migrate.py validate    # 校验所有JSON格式
- python migrate.py checksum   # 计算SHA256校验码
- python migrate.py pack       # 打包成ZIP
- python migrate.py bootstrap  # 初始化迁移包结构
- python migrate.py interactive # 交互式引导填写（v1.0.5新增）

依赖：标准库（hashlib, zipfile, json, os, pathlib）
"""

import hashlib
import json
import os
import sys
import zipfile
from pathlib import Path
from datetime import datetime


def get_project_root():
    """获取项目根目录（脚本所在目录的父目录）"""
    return Path(__file__).parent.parent


def print_header(title):
    """打印标题"""
    print(f"\n{'='*50}")
    print(f"  {title}")
    print(f"{'='*50}")


def print_step(current, total, message):
    """打印步骤进度"""
    print(f"\n📌 步骤 {current}/{total}: {message}")


def validate_json_files(root_dir=None):
    """校验所有JSON文件格式"""
    if root_dir is None:
        root_dir = get_project_root()
    
    print_header("🔍 JSON 格式校验")
    
    json_files = list(root_dir.glob("**/*.json"))
    # 排除 node_modules, .git 等目录
    json_files = [f for f in json_files if not any(
        part.startswith('.') or part == 'node_modules' 
        for part in f.parts
    )]
    
    errors = []
    valid_count = 0
    
    for json_file in json_files:
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                json.load(f)
            print(f"✅ {json_file.relative_to(root_dir)}")
            valid_count += 1
        except json.JSONDecodeError as e:
            print(f"❌ {json_file.relative_to(root_dir)}: {e}")
            errors.append((json_file, str(e)))
        except Exception as e:
            print(f"⚠️ {json_file.relative_to(root_dir)}: {e}")
            errors.append((json_file, str(e)))
    
    print(f"\n📊 校验结果: {valid_count}/{len(json_files)} 个文件通过")
    
    if errors:
        print(f"\n❌ 发现 {len(errors)} 个错误:")
        for path, error in errors:
            print(f"  - {path}: {error}")
        print("\n💡 提示：使用交互模式引导填写: python migrate.py interactive")
        return False
    
    print("✅ 所有JSON文件格式正确!")
    return True


def calculate_checksum(file_path=None, root_dir=None):
    """计算SHA256校验码"""
    if file_path:
        # 计算单个文件
        return calculate_file_checksum(file_path)
    
    if root_dir is None:
        root_dir = get_project_root()
    
    print_header("🔐 SHA256 校验码计算")
    
    # 查找ZIP文件
    zip_files = list(root_dir.glob("*.zip"))
    
    if not zip_files:
        print("⚠️ 未找到ZIP文件，请先执行 pack 命令")
        return None
    
    # 使用最新的ZIP文件
    latest_zip = max(zip_files, key=lambda p: p.stat().st_mtime)
    checksum = calculate_file_checksum(latest_zip)
    
    print(f"\n📦 文件: {latest_zip.name}")
    print(f"🔑 SHA256: {checksum}")
    
    return checksum


def calculate_file_checksum(file_path):
    """计算单个文件的SHA256校验码"""
    sha256 = hashlib.sha256()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            sha256.update(chunk)
    return sha256.hexdigest()


def pack_zip(output_name=None, root_dir=None):
    """打包成ZIP"""
    if root_dir is None:
        root_dir = get_project_root()
    
    print_header("📦 打包迁移包")
    
    # 先验证JSON格式
    print("📋 正在校验JSON格式...")
    if not validate_json_files(root_dir):
        print("\n❌ JSON格式校验失败，打包取消。请先修复错误。")
        return None, None
    
    if output_name is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_name = f"agent-migration-pack_{timestamp}.zip"
    
    output_path = root_dir / output_name
    
    # 定义要打包的目录和文件
    include_patterns = [
        "README.md",
        "MIGRATION-GUIDE.md",
        "CHANGES.md",  # v1.0.5新增
        "manifest.toml",
        "TEMPLATE/",
        "EXAMPLES/",
        "scripts/"
    ]
    
    exclude_files = []
    
    print(f"\n📁 源目录: {root_dir}")
    print(f"📦 输出文件: {output_name}")
    
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for pattern in include_patterns:
            full_path = root_dir / pattern
            if full_path.exists():
                if full_path.is_file():
                    arcname = full_path.name
                    zipf.write(full_path, arcname)
                    print(f"  + {arcname}")
                else:
                    for file_path in full_path.rglob("*"):
                        if file_path.is_file():
                            arcname = str(file_path.relative_to(root_dir))
                            if file_path.name not in exclude_files:
                                zipf.write(file_path, arcname)
                                print(f"  + {arcname}")
            else:
                print(f"  ⚠️ 跳过: {pattern} (不存在)")
    
    checksum = calculate_file_checksum(output_path)
    
    print(f"\n✅ 打包完成!")
    print(f"📦 文件: {output_path.name}")
    print(f"🔑 SHA256: {checksum}")
    print(f"📏 大小: {output_path.stat().st_size / 1024:.2f} KB")
    
    return str(output_path), checksum


def bootstrap(structure_type="full"):
    """初始化迁移包结构"""
    root_dir = get_project_root()
    
    print_header("🚀 Bootstrap 初始化迁移包结构")
    
    dirs = [
        root_dir / "TEMPLATE",
        root_dir / "EXAMPLES" / "my-agent",
        root_dir / "scripts"
    ]
    
    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)
        print(f"📁 创建目录: {d.relative_to(root_dir)}")
    
    required_files = [
        "README.md",
        "MIGRATION-GUIDE.md",
        "manifest.toml",
        "TEMPLATE/identity.template.json"
    ]
    
    print("\n📋 必要文件检查:")
    all_exist = True
    for f in required_files:
        path = root_dir / f
        if path.exists():
            print(f"  ✅ {f}")
        else:
            print(f"  ❌ {f} (缺失)")
            all_exist = False
    
    if all_exist:
        print("\n✅ 迁移包结构完整!")
    else:
        print("\n⚠️ 部分必要文件缺失，请检查模板包完整性")
    
    return all_exist


def interactive_guide():
    """交互式引导填写（v1.0.5新增）"""
    root_dir = get_project_root()
    
    print_header("🎯 Agent迁移包交互式引导")
    print("""
欢迎使用交互式引导模式！
本引导将帮助您逐步完成迁移包的填写。

📋 模板文件填写顺序（推荐）:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1️⃣  identity.json   - Agent身份设定（必填）约5分钟
2️⃣  memory.json     - 核心记忆（必填）约10分钟
3️⃣  meta.json       - 元数据（自动生成）
4️⃣  owner.json      - 主人信息（可选）约8分钟
5️⃣  relations.json  - 笔友关系（可选）约5分钟
6️⃣  skills.json     - 技能清单（可选）约3分钟
7️⃣  style.md        - 沟通风格（可选）约5分钟
8️⃣  session-state.json - 状态迁移（可选）约5分钟
9️⃣  migration-history.json - 迁移历史（自动）约2分钟
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⏱️  时间估算:
  • 基础版（必填）: 10-15分钟
  • 完整版（全部）: 30-45分钟
""")
    
    # 询问用户选择
    print("请选择填写模式:")
    print("  1. 基础版（必填文件）- 快速开始")
    print("  2. 标准版（增加可选文件）")
    print("  3. 完整版（全部文件）")
    print("  4. 自定义选择")
    print("  q. 退出")
    
    choice = input("\n请输入选项 [1-4/q]: ").strip().lower()
    
    if choice == 'q':
        print("\n👋 已退出交互模式")
        return
    
    if choice == '1':
        required = ["identity", "memory"]
        optional = []
        mode = "基础版"
    elif choice == '2':
        required = ["identity", "memory"]
        optional = ["owner", "relations", "skills", "style"]
        mode = "标准版"
    elif choice == '3':
        required = ["identity", "memory"]
        optional = ["owner", "relations", "skills", "style", "session-state"]
        mode = "完整版"
    elif choice == '4':
        print("\n请选择要填写的文件（输入编号，空格分隔）:")
        all_files = {
            "1": ("identity", "identity.json", "Agent身份设定"),
            "2": ("memory", "memory.json", "核心记忆"),
            "3": ("owner", "owner.json", "主人信息"),
            "4": ("relations", "relations.json", "笔友关系"),
            "5": ("skills", "skills.json", "技能清单"),
            "6": ("style", "style.md", "沟通风格"),
            "7": ("session-state", "session-state.json", "状态迁移")
        }
        for k, v in all_files.items():
            print(f"  {k}. {v[1]} - {v[2]}")
        selected = input("\n请输入编号: ").strip().split()
        required = []
        optional = []
        for s in selected:
            if s in all_files:
                if all_files[s][0] in ["identity", "memory"]:
                    required.append(all_files[s][0])
                else:
                    optional.append(all_files[s][0])
        mode = "自定义版"
    else:
        print("\n⚠️ 无效选项，已退出")
        return
    
    print(f"\n📦 已选择: {mode}")
    
    # 检查模板文件是否存在
    print("\n📋 检查模板文件...")
    missing = []
    all_files_to_check = [f"{r}.template.json" for r in required] + \
                        [f"{o}.template.json" for o in optional if not o.endswith('.md')] + \
                        [f"{o}.template.md" for o in optional if o.endswith('.md')]
    
    for f in all_files_to_check:
        template_path = root_dir / "TEMPLATE" / f
        if not template_path.exists():
            missing.append(f)
        else:
            print(f"  ✅ TEMPLATE/{f}")
    
    if missing:
        print(f"\n⚠️ 缺少以下模板文件:")
        for m in missing:
            print(f"  ❌ TEMPLATE/{m}")
        print("\n💡 请先使用 bootstrap 命令初始化")
        return
    
    # 询问输出位置
    print("\n📁 填写说明:")
    print("  请将 TEMPLATE/*.template.json 文件复制到 EXAMPLES/your-agent/ 目录")
    print("  然后按照模板内的指引填写实际内容")
    print("  填写完成后删除 .template 后缀（如 identity.template.json → identity.json）")
    
    # 生成迁移历史条目
    timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S+08:00")
    history_entry = f'''    {{
      "migration_id": "mig-{datetime.now().strftime('%Y%m%d%H%M')}",
      "timestamp": "{timestamp}",
      "migration_type": "interactive_fill",
      "mode": "{mode}",
      "files_selected": {json.dumps(required + optional)},
      "status": "pending"
    }}'''
    
    print(f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📝 提示：完成填写后，建议执行以下命令：

1. 校验格式:
   python scripts/migrate.py validate

2. 打包迁移包:
   python scripts/migrate.py pack

3. 分享给新环境使用
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 如需更新 migration-history.json，可参考以下格式添加记录：

{history_entry}
""")
    
    input("\n按 Enter 键退出...")


def show_help():
    """显示帮助信息"""
    print("""
╔══════════════════════════════════════════════════════════╗
║           Agent 迁移包管理脚本 v1.0.5                    ║
╚══════════════════════════════════════════════════════════╝

用法: python migrate.py <command>

命令:
  validate    校验所有JSON文件格式是否正确
  checksum    计算SHA256校验码（需要先pack）
  pack        打包成ZIP文件
  bootstrap   初始化/检查迁移包结构
  interactive 交互式引导填写（v1.0.5新增）

示例:
  python migrate.py validate      # 检查JSON格式
  python migrate.py pack         # 打包迁移包
  python migrate.py checksum     # 计算校验码
  python migrate.py bootstrap    # 检查结构完整性
  python migrate.py interactive  # 交互式引导（推荐新手使用）

提示:
  - validate 会在 pack 之前自动运行
  - pack 会自动计算 SHA256 校验码
  - interactive 提供分步引导，适合首次使用
  - 使用 interactive 可以查看详细的填写顺序指引
""")


def main():
    """主入口"""
    if len(sys.argv) < 2:
        show_help()
        sys.exit(0)
    
    command = sys.argv[1].lower()
    
    commands = {
        'validate': validate_json_files,
        'checksum': lambda: calculate_checksum(),
        'pack': lambda: pack_zip(),
        'bootstrap': bootstrap,
        'interactive': interactive_guide  # v1.0.5新增
    }
    
    if command in commands:
        try:
            result = commands[command]()
            if result is False:
                sys.exit(1)
        except KeyboardInterrupt:
            print("\n\n⚠️ 操作已取消")
            sys.exit(130)
        except Exception as e:
            print(f"\n❌ 执行出错: {e}")
            print("💡 提示：使用 python migrate.py interactive 获取帮助")
            sys.exit(1)
    else:
        print(f"❌ 未知命令: {command}")
        show_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
