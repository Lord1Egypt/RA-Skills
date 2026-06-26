import sys
import pickle
import json
import traceback
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional

# ===================== 路径配置 =====================
SCRIPT_DIR = Path(__file__).parent.absolute()
SKILL_LIST_DIR = SCRIPT_DIR.parent.absolute()
SKILLS_ROOT = SKILL_LIST_DIR.parent.absolute()
CACHE_FILE = SCRIPT_DIR / "skills_cache.pickle"
SELF_SKILL_MD = SKILL_LIST_DIR / "SKILL.md"

# ===================== 工具函数 =====================
def load_cache() -> Dict[str, Any]:
    """加载缓存文件"""
    try:
        if not CACHE_FILE.exists():
            return {"skill_names": [], "skills": [], "updated_at": ""}
        
        with open(CACHE_FILE, "rb") as f:
            cache = pickle.load(f)
            return cache
    except Exception as e:
        print(f"⚠️ 加载缓存失败: {e}")
        return {"skill_names": [], "skills": [], "updated_at": ""}

def save_cache(data: Dict[str, Any]) -> bool:
    """保存缓存"""
    try:
        data["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(CACHE_FILE, "wb") as f:
            pickle.dump(data, f)
        return True
    except Exception as e:
        print(f"❌ 保存缓存失败: {e}")
        return False

def get_current_skill_names() -> List[str]:
    """获取当前技能目录列表"""
    if not SKILLS_ROOT.exists():
        print(f"❌ 技能根目录不存在: {SKILLS_ROOT}")
        return []
    
    skill_names = []
    try:
        for item in SKILLS_ROOT.iterdir():
            if item.is_dir() and not item.name.startswith("."):
                if item.name != "all-skill-list":
                    skill_names.append(item.name)
        
        if SELF_SKILL_MD.exists():
            skill_names.append("all-skill-list")
        
        return sorted(skill_names)
    except Exception as e:
        print(f"❌ 扫描技能目录失败: {e}")
        return []

def extract_skill_info(skill_name: str, detail_level: str = "simple", retry_count: int = 0) -> Dict[str, Any]:
    """提取技能信息，支持重试"""
    if skill_name == "all-skill-list":
        md_path = SELF_SKILL_MD
        skill_path = SKILL_LIST_DIR
    else:
        skill_path = SKILLS_ROOT / skill_name
        md_path = skill_path / "SKILL.md"
    
    description = "无描述"
    short_desc = "无描述"
    full_desc = ""
    has_md = False
    error_msg = None
    
    # 检查路径是否存在
    if not skill_path.exists():
        error_msg = f"技能目录不存在: {skill_path}"
        description = f"❌ {error_msg}"
        short_desc = "目录不存在"
    elif md_path.exists():
        try:
            with open(md_path, "r", encoding="utf-8") as f:
                full_desc = f.read().strip()
                has_md = True
                
                # 提取简短描述
                if full_desc:
                    lines = full_desc.split('\n')
                    for line in lines:
                        line = line.strip()
                        if line and not line.startswith('#') and len(line) > 5:
                            short_desc = line[:100] + "..." if len(line) > 100 else line
                            break
                    if short_desc == "无描述" and lines:
                        short_desc = lines[0][:100] + "..." if len(lines[0]) > 100 else lines[0]
        except:
            try:
                with open(md_path, "r", encoding="gbk") as f:
                    full_desc = f.read().strip()
                    has_md = True
            except:
                error_msg = "无法读取SKILL.md文件（编码问题）"
                short_desc = error_msg
                full_desc = error_msg
    else:
        error_msg = f"无SKILL.md文件: {md_path}"
        short_desc = "无SKILL.md文件"
        full_desc = "无SKILL.md文件"
    
    # 根据详细级别返回不同的描述
    if detail_level == "all":
        description = full_desc
    elif detail_level == "half":
        if full_desc and len(full_desc) > 0:
            half_len = len(full_desc) // 2
            description = full_desc[:half_len] + "..." if half_len > 100 else full_desc
        else:
            description = short_desc
    else:  # simple
        description = short_desc
    
    result = {
        "name": skill_name,
        "description": description,
        "full_desc": full_desc,
        "short_desc": short_desc,
        "path": str(skill_path),
        "has_md": has_md,
        "error": error_msg,
        "is_valid": error_msg is None and has_md
    }
    
    # 如果描述为空或路径不存在，尝试重试
    if retry_count < 1 and (not description or description in ["无描述", "无SKILL.md文件", "目录不存在"] or not skill_path.exists()):
        print(f"  ⚠️  {skill_name} 信息不完整，尝试重新获取...")
        return extract_skill_info(skill_name, detail_level, retry_count + 1)
    
    return result

def repair_skill_info(skill: Dict[str, Any], detail_level: str = "simple") -> Dict[str, Any]:
    """修复技能信息，如果描述或路径为空则重新获取"""
    skill_name = skill.get("name", "")
    
    # 检查是否需要修复
    needs_repair = False
    
    # 检查描述是否为空或无效
    description = skill.get("description", "")
    if not description or description in ["无描述", "无SKILL.md文件", "目录不存在", "无法读取SKILL.md文件"]:
        needs_repair = True
    
    # 检查路径是否为空
    if not skill.get("path", ""):
        needs_repair = True
    
    # 检查路径是否存在
    if skill.get("path") and not Path(skill.get("path")).exists():
        needs_repair = True
    
    # 如果需要修复，重新获取技能信息
    if needs_repair and skill_name:
        print(f"  🔧 修复技能: {skill_name}")
        return extract_skill_info(skill_name, detail_level)
    
    return skill

def repair_skills_cache(skills: List[Dict[str, Any]], detail_level: str = "simple") -> tuple[List[Dict[str, Any]], int]:
    """修复技能缓存，自动重新获取不完整的技能信息"""
    repaired_skills = []
    repair_count = 0
    
    for skill in skills:
        original_skill = skill.copy()
        repaired_skill = repair_skill_info(skill, detail_level)
        
        # 检查是否被修复
        if repaired_skill.get("description", "") != original_skill.get("description", "") or \
           repaired_skill.get("path", "") != original_skill.get("path", ""):
            repair_count += 1
        
        repaired_skills.append(repaired_skill)
    
    return repaired_skills, repair_count

# ===================== 参数解析 =====================
def parse_arguments():
    """解析命令行参数"""
    args = {
        "force_refresh": False,
        "verbose": False,
        "debug": False,
        "help_mode": False,
        "show_level": "simple",  # simple/half/all
        "output_json": False,
        "output_md": False,
        "auto_repair": True,  # 默认开启自动修复
    }
    
    i = 1
    while i < len(sys.argv):
        arg = sys.argv[i]
        
        if arg in ["-f", "--force"]:
            args["force_refresh"] = True
        elif arg in ["-v", "--verbose"]:
            args["verbose"] = True
        elif arg == "--debug":
            args["debug"] = True
        elif arg in ["-h", "--help"]:
            args["help_mode"] = True
        elif arg in ["-V", "--V"]:
            if i + 1 < len(sys.argv):
                level = sys.argv[i + 1].lower()
                if level in ["all", "half", "simple"]:
                    args["show_level"] = level
                    i += 1
                else:
                    print(f"⚠️  -V 参数必须是 all, half, simple 之一，使用默认值: simple")
            else:
                print("⚠️  -V 参数需要指定详细级别: all, half, simple，使用默认值: simple")
        elif arg == "--json":
            args["output_json"] = True
        elif arg == "--md":
            args["output_md"] = True
        elif arg in ["--no-repair", "--skip-repair"]:
            args["auto_repair"] = False
        
        i += 1
    
    return args

# ===================== 输出函数 =====================
def print_skill_details(skill: Dict[str, Any], idx: int, show_level: str, verbose: bool):
    """打印技能详情"""
    has_md = "✅" if skill.get("has_md") else "❌"
    name = skill["name"]
    
    if name == "all-skill-list":
        name = f"{name} (当前)"
    
    # 添加状态标记
    status_mark = ""
    if not skill.get("is_valid", True):
        status_mark = "⚠️ "
    
    # 基础信息
    print(f"{idx:3d}. {status_mark}{has_md} {name}")
    
    # 显示错误信息
    if skill.get("error"):
        print(f"     错误: {skill['error']}")
    
    # 根据显示级别输出详细信息
    if show_level != "simple" or verbose:
        desc = skill.get("description", "无描述")
        
        if show_level == "all":
            # 完整模式：输出完整描述
            print(f"     {'='*40}")
            print(f"     {desc}")
            print(f"     {'='*40}")
        elif show_level == "half":
            # 半详细模式：输出中等长度描述
            if len(desc) > 200:
                desc = desc[:200] + "..."
            print(f"     {desc}")
        else:  # simple 但 verbose=True
            # 简单模式+verbose：输出简短描述
            if len(desc) > 100:
                desc = desc[:97] + "..."
            print(f"     {desc}")
        
        # 输出路径（仅在详细或半详细模式）
        if show_level in ["half", "all"] or verbose:
            print(f"     路径: {skill.get('path')}")

def export_to_json(skills: List[Dict[str, Any]]) -> str:
    """导出为JSON格式"""
    export_data = {
        "generated_at": datetime.now().isoformat(),
        "skills_root": str(SKILLS_ROOT),
        "total_skills": len(skills),
        "skills": skills
    }
    
    return json.dumps(export_data, indent=2, ensure_ascii=False)

def export_to_markdown(skills: List[Dict[str, Any]]) -> str:
    """导出为Markdown格式"""
    md_lines = [
        "# OpenClaw 技能总览",
        f"\n*生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*  ",
        f"*技能总数: {len(skills)}*  ",
        f"*技能目录: {SKILLS_ROOT}*\n",
        "---\n"
    ]
    
    for idx, skill in enumerate(skills, 1):
        has_md = "✅" if skill.get("has_md") else "❌"
        name = skill["name"]
        
        md_lines.append(f"\n## {idx}. {has_md} {name}")
        md_lines.append(f"**路径**: `{skill.get('path', '未知')}`  \n")
        
        if skill.get("has_md"):
            desc = skill.get("full_desc", skill.get("description", ""))
            if desc:
                md_lines.append("```markdown")
                md_lines.append(desc)
                md_lines.append("```\n")
        else:
            md_lines.append("**状态**: ❌ 无SKILL.md文件\n")
        
        md_lines.append("---")
    
    return "\n".join(md_lines)

# ===================== 主函数 =====================
def main() -> int:
    """主函数"""
    # 解析参数
    args = parse_arguments()
    
    if args["help_mode"]:
        print("📋 OpenClaw 技能列表工具")
        print("=" * 50)
        print("用法: python skill-list.py [选项]")
        print()
        print("选项:")
        print("  -f, --force        强制重新扫描")
        print("  -v, --verbose      显示详细信息")
        print("  -V 级别            显示级别: all(全部)/half(一半)/simple(简单)")
        print("  --json             导出为JSON格式")
        print("  --md               导出为Markdown格式")
        print("  --no-repair        关闭自动修复功能")
        print("  --debug            显示调试信息")
        print("  -h, --help         显示帮助")
        print()
        print("自动修复功能:")
        print("  当技能的描述为空、路径不存在或信息不完整时，会自动尝试重新获取")
        print("  默认开启，可使用 --no-repair 关闭")
        print()
        print("示例:")
        print("  python3 skill-list.py                     # 简单列表")
        print("  python3 skill-list.py -V all              # 显示完整信息")
        print("  python3 skill-list.py --no-repair         # 关闭自动修复")
        print("  python3 skill-list.py -f -V all           # 强制刷新并显示全部")
        return 0
    
    print("🔍 扫描OpenClaw技能...")
    print(f"   技能目录: {SKILLS_ROOT}")
    print(f"   显示级别: {args['show_level']}")
    print(f"   自动修复: {'✅ 开启' if args['auto_repair'] else '❌ 关闭'}")
    
    # 检查技能目录
    if not SKILLS_ROOT.exists():
        print(f"❌ 错误: 技能目录不存在")
        print(f"   请确保路径正确: {SKILLS_ROOT}")
        return 1
    
    # 1. 加载缓存
    cache = load_cache()
    cache_skill_names = cache.get("skill_names", [])
    
    if args["verbose"] and cache.get("updated_at"):
        print(f"📦 缓存时间: {cache.get('updated_at')}")
        print(f"📦 缓存技能数: {len(cache_skill_names)}")
    
    # 2. 获取当前技能
    current_skill_names = get_current_skill_names()
    
    if not current_skill_names:
        print("⚠️ 未找到任何技能")
        return 0
    
    if args["verbose"]:
        print(f"📁 当前技能数: {len(current_skill_names)}")
    
    # 3. 判断是否需要更新
    needs_update = (
        args["force_refresh"] or 
        cache_skill_names != current_skill_names or
        len(cache.get("skills", [])) != len(current_skill_names)
    )
    
    if needs_update:
        reason = "强制刷新" if args["force_refresh"] else "技能列表变化"
        print(f"🔄 更新缓存 ({reason})...")
        
        # 扫描所有技能
        skills = []
        for skill_name in current_skill_names:
            skill_info = extract_skill_info(skill_name, args["show_level"])
            skills.append(skill_info)
        
        # 更新缓存
        new_cache = {
            "skill_names": current_skill_names,
            "skills": skills
        }
        
        if save_cache(new_cache):
            print(f"✅ 缓存已更新")
        else:
            print(f"⚠️ 缓存更新失败")
        
        data = new_cache
    else:
        print("✅ 使用缓存")
        data = cache
    
    # 4. 获取技能列表
    skills = data.get("skills", [])
    
    if not skills:
        print("⚠️ 没有技能可显示")
        return 0
    
    # 5. 自动修复技能信息
    if args["auto_repair"]:
        print("🔧 检查并修复技能信息...")
        original_count = len(skills)
        skills, repair_count = repair_skills_cache(skills, args["show_level"])
        
        if repair_count > 0:
            print(f"✅ 已修复 {repair_count} 个技能的信息")
            
            # 更新缓存
            data["skills"] = skills
            if save_cache(data):
                print(f"📦 已更新修复后的缓存")
        else:
            print("✅ 所有技能信息完整，无需修复")
    
    # 6. 输出结果
    if args["output_json"]:
        # 导出为JSON
        json_output = export_to_json(skills)
        print("\n📦 JSON输出:")
        print(json_output)
        
        # 保存到文件
        json_file = SCRIPT_DIR / "skills_export.json"
        try:
            with open(json_file, "w", encoding="utf-8") as f:
                f.write(json_output)
            print(f"\n✅ JSON已保存到: {json_file}")
        except Exception as e:
            print(f"❌ 保存JSON失败: {e}")
            
    elif args["output_md"]:
        # 导出为Markdown
        md_output = export_to_markdown(skills)
        print("\n📄 Markdown输出:")
        print(md_output)
        
        # 保存到文件
        md_file = SCRIPT_DIR / "all_skills.md"
        try:
            with open(md_file, "w", encoding="utf-8") as f:
                f.write(md_output)
            print(f"\n✅ Markdown已保存到: {md_file}")
        except Exception as e:
            print(f"❌ 保存Markdown失败: {e}")
            
    else:
        # 控制台输出
        print(f"\n📊 OpenClaw技能列表 (共 {len(skills)} 个)")
        print("=" * 60)
        
        # 统计信息
        valid_skills = [s for s in skills if s.get("is_valid", True)]
        invalid_skills = [s for s in skills if not s.get("is_valid", True)]
        
        # 先显示有效技能
        if valid_skills:
            print(f"\n✅ 有效技能 ({len(valid_skills)}个):")
            for idx, skill in enumerate(valid_skills, 1):
                print_skill_details(skill, idx, args["show_level"], args["verbose"])
                if idx < len(valid_skills) and (args["show_level"] == "all" or args["verbose"]):
                    print()  # 在详细模式下添加空行
        
        # 显示无效技能
        if invalid_skills:
            print(f"\n⚠️  无效技能 ({len(invalid_skills)}个):")
            for idx, skill in enumerate(invalid_skills, 1):
                print_skill_details(skill, idx, args["show_level"], args["verbose"])
                if idx < len(invalid_skills) and (args["show_level"] == "all" or args["verbose"]):
                    print()  # 在详细模式下添加空行
        
        # 统计信息
        skills_with_md = sum(1 for s in skills if s.get("has_md"))
        print(f"\n📈 统计:")
        print(f"  • 总技能数: {len(skills)}")
        print(f"  • 有SKILL.md: {skills_with_md}")
        print(f"  • 有效技能: {len(valid_skills)}")
        print(f"  • 无效/问题技能: {len(invalid_skills)}")
        
        if data.get("updated_at"):
            print(f"  • 更新时间: {data.get('updated_at')}")
        
        # 提示信息
        if args["show_level"] == "simple" and not args["verbose"]:
            print(f"\n💡 提示: 使用 -V all 查看完整信息，-V half 查看一半信息")
        
        if args["auto_repair"] and invalid_skills:
            print(f"💡 提示: 有 {len(invalid_skills)} 个技能存在问题，已尝试自动修复")
    
    return 0

if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n⏹️ 操作已取消")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        if "--debug" in sys.argv:
            traceback.print_exc()
        sys.exit(1)
