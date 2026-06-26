"""
快递追踪管理脚本
用法:
  python manage.py add <单号> [备注]    添加追踪
  python manage.py remove <单号>        移除追踪
  python manage.py list                 列出所有
  python manage.py refresh              刷新全部追踪中的快递
  python manage.py clean                清理已签收超过7天的记录
"""
import sys, json, os
from datetime import datetime, timedelta

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

# 导入 track 模块的查询功能和数据访问
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from track import query_express, format_result, load_packages, save_packages

def cmd_add(tracking_number, label=""):
    """添加快递追踪"""
    data = load_packages()
    
    for pkg in data["packages"]:
        if pkg["tracking_number"] == tracking_number:
            if label:
                pkg["label"] = label
                save_packages(data)
                print(f"✅ 已更新备注: {tracking_number} → {label}")
            else:
                print(f"⏭️ {tracking_number} 已在追踪列表中")
            return
    
    # 先查询一次获取快递公司
    result = query_express(tracking_number)
    if "error" in result:
        # 查询失败也添加，标记为待查询
        courier_code = "auto"
        courier_name = "待识别"
    else:
        courier_code = result["courier_code"]
        courier_name = result["courier"]
    
    data["packages"].append({
        "tracking_number": tracking_number,
        "courier_code": courier_code,
        "courier_name": courier_name,
        "label": label,
        "added_at": datetime.now().isoformat(),
        "last_status": result.get("status", "待查询"),
        "last_update": datetime.now().isoformat(),
        "traces": result.get("traces", []),
        "delivered": result.get("delivered", False)
    })
    
    save_packages(data)
    print(f"✅ 已添加: {courier_name} {tracking_number}" + (f" ({label})" if label else ""))

def cmd_remove(tracking_number):
    """移除快递追踪"""
    data = load_packages()
    original_count = len(data["packages"])
    data["packages"] = [p for p in data["packages"] if p["tracking_number"] != tracking_number]
    
    if len(data["packages"]) < original_count:
        save_packages(data)
        print(f"✅ 已移除: {tracking_number}")
    else:
        print(f"❌ 未找到: {tracking_number}")

def cmd_list():
    """列出所有追踪中的快递"""
    data = load_packages()
    
    if not data["packages"]:
        print("📭 追踪列表为空")
        print("使用 'python manage.py add <单号>' 添加快递")
        return data
    
    active = [p for p in data["packages"] if not p["delivered"]]
    delivered = [p for p in data["packages"] if p["delivered"]]
    
    print(f"📦 快递追踪列表 (共 {len(data['packages'])} 个)")
    print(f"   在途: {len(active)} | 已签收: {len(delivered)}")
    print()
    
    if active:
        print("🚚 在途快递:")
        for i, pkg in enumerate(active, 1):
            label = f" ({pkg['label']})" if pkg.get("label") else ""
            print(f"  {i}. {pkg['courier_name']} {pkg['tracking_number']}{label}")
            print(f"     状态: {pkg['last_status']} | 更新: {pkg['last_update'][:16]}")
        print()
    
    if delivered:
        print("✅ 已签收:")
        for i, pkg in enumerate(delivered, 1):
            label = f" ({pkg['label']})" if pkg.get("label") else ""
            print(f"  {i}. {pkg['courier_name']} {pkg['tracking_number']}{label}")
    
    return data

def cmd_refresh():
    """刷新所有未签收的快递状态"""
    data = load_packages()
    active = [p for p in data["packages"] if not p["delivered"]]
    
    if not active:
        print("📭 没有需要刷新的快递，全部已签收")
        return
    
    print(f"🔄 正在刷新 {len(active)} 个快递...")
    updated = 0
    newly_delivered = 0
    
    for pkg in active:
        tn = pkg["tracking_number"]
        print(f"   查询 {tn}...", end=" ")
        
        result = query_express(tn)
        if "error" in result:
            print(f"❌ {result['error']}")
        else:
            old_status = pkg["last_status"]
            new_status = result["status"]
            if old_status != new_status:
                print(f"📝 {old_status} → {new_status}")
                updated += 1
                if result["delivered"] and not pkg["delivered"]:
                    newly_delivered += 1
                    print(f"   🎉 {tn} 已签收！")
            else:
                print(f"   {new_status} (无变化)")
    
    save_packages(data)
    print(f"\n✅ 刷新完成: {updated} 个状态更新, {newly_delivered} 个新签收")

def cmd_clean():
    """清理已签收超过7天的记录"""
    data = load_packages()
    cutoff = datetime.now() - timedelta(days=7)
    old_count = len(data["packages"])
    
    kept = []
    removed = []
    for pkg in data["packages"]:
        if pkg["delivered"]:
            try:
                added = datetime.fromisoformat(pkg["added_at"])
                if added < cutoff:
                    removed.append(pkg)
                    continue
            except:
                pass
        kept.append(pkg)
    
    data["packages"] = kept
    save_packages(data)
    print(f"✅ 清理完成: 移除 {len(removed)} 条已签收记录，保留 {len(kept)} 条")

def main():
    if len(sys.argv) < 2:
        print("快递追踪管理工具")
        print("用法:")
        print("  python manage.py add <单号> [备注]")
        print("  python manage.py remove <单号>")
        print("  python manage.py list")
        print("  python manage.py refresh")
        print("  python manage.py clean")
        sys.exit(1)
    
    cmd = sys.argv[1].lower()
    
    if cmd == "add":
        if len(sys.argv) < 3:
            print("❌ 请提供快递单号")
            sys.exit(1)
        tn = sys.argv[2]
        label = sys.argv[3] if len(sys.argv) > 3 else ""
        cmd_add(tn, label)
    
    elif cmd == "remove":
        if len(sys.argv) < 3:
            print("❌ 请提供快递单号")
            sys.exit(1)
        cmd_remove(sys.argv[2])
    
    elif cmd == "list":
        cmd_list()
    
    elif cmd == "refresh":
        cmd_refresh()
    
    elif cmd == "clean":
        cmd_clean()
    
    else:
        print(f"❌ 未知命令: {cmd}")
        sys.exit(1)

if __name__ == "__main__":
    main()
