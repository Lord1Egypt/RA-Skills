from analyze import analyze_all
from commit import commit

def main():
    commit_type = input("提交类型: ")
    message = input("提交说明: ")
    version = input("版本号: ")
    module = input("模块名称: ")

    total, ai, percent = analyze_all()

    print(f"统计：{total} / {ai} / {percent}%")

    confirm = input("确认提交? (y/n): ")
    if confirm.lower() != "y":
        print("取消")
        return

    msg = commit(commit_type, message, version, module, total, ai, percent)
    print("\n提交成功：\n")
    print(msg)

if __name__ == "__main__":
    main()