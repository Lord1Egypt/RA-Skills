import requests

APP_ID = "your_feishu_app_id"
APP_SECRET = "your_feishu_app_secret"

BASE_URL = "https://open.feishu.cn/open-apis"


def get_tenant_access_token():
    url = f"{BASE_URL}/auth/v3/tenant_access_token/internal"
    resp = requests.post(url, json={
        "app_id": APP_ID,
        "app_secret": APP_SECRET,
    })
    data = resp.json()
    if data.get("code") != 0:
        raise Exception(f"获取 token 失败: {data}")
    return data["tenant_access_token"]


def create_bitable(token):
    """创建多维表格"""
    url = f"{BASE_URL}/bitable/v1/apps"
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.post(url, headers=headers, json={
        "name": "今日头条文章收藏",
    })
    data = resp.json()
    if data.get("code") != 0:
        raise Exception(f"创建多维表格失败: {data}")
    app = data["data"]["app"]
    print(f"多维表格创建成功!")
    print(f"  名称: {app['name']}")
    print(f"  链接: {app.get('url', 'N/A')}")
    return app["app_token"], app["default_table_id"]


def add_fields(token, app_token, table_id):
    """添加字段"""
    url = f"{BASE_URL}/bitable/v1/apps/{app_token}/tables/{table_id}/fields"
    headers = {"Authorization": f"Bearer {token}"}

    fields = [
        {
            "field_name": "文章链接",
            "type": 15,  # 超链接
        },
        {
            "field_name": "文章ID",
            "type": 1,  # 文本（用于去重检索）
        },
        {
            "field_name": "分享人",
            "type": 1,  # 文本
        },
        {
            "field_name": "分享时间",
            "type": 5,  # 日期
            "property": {
                "date_formatter": "yyyy/MM/dd",
                "auto_fill": True,
            },
        },
        {
            "field_name": "分类标签",
            "type": 3,  # 单选
            "property": {
                "options": [
                    {"name": "科技"},
                    {"name": "财经"},
                    {"name": "娱乐"},
                    {"name": "健康"},
                    {"name": "教育"},
                    {"name": "体育"},
                    {"name": "其他"},
                ]
            },
        },
        {
            "field_name": "备注",
            "type": 1,  # 文本
        },
        {
            "field_name": "已读",
            "type": 7,  # 复选框
        },
    ]

    for field in fields:
        resp = requests.post(url, headers=headers, json=field)
        data = resp.json()
        if data.get("code") != 0:
            print(f"  添加字段 '{field['field_name']}' 失败: {data}")
        else:
            print(f"  添加字段 '{field['field_name']}' 成功")


def rename_first_field(token, app_token, table_id):
    """将默认的第一个字段重命名为'文章标题'"""
    url = f"{BASE_URL}/bitable/v1/apps/{app_token}/tables/{table_id}/fields"
    headers = {"Authorization": f"Bearer {token}"}

    resp = requests.get(url, headers=headers)
    data = resp.json()
    if data.get("code") != 0:
        print(f"  获取字段列表失败: {data}")
        return

    first_field = data["data"]["items"][0]
    field_id = first_field["field_id"]

    update_url = f"{url}/{field_id}"
    resp = requests.put(update_url, headers=headers, json={
        "field_name": "文章标题",
        "type": first_field["type"],
    })
    data = resp.json()
    if data.get("code") != 0:
        print(f"  重命名字段失败: {data}")
    else:
        print(f"  重命名默认字段为 '文章标题' 成功")


def grant_user_access(token, app_token, user_open_id):
    """授予用户对多维表格的完全访问权限"""
    url = f"{BASE_URL}/drive/v1/permissions/{app_token}/members?type=bitable&need_notification=false"
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.post(url, headers=headers, json={
        "member_type": "openid",
        "member_id": user_open_id,
        "perm": "full_access",
    })
    data = resp.json()
    if data.get("code") != 0:
        print(f"  授权失败: {data}")
    else:
        print(f"  已授予用户 {user_open_id} 完全访问权限")


def main():
    # 飞书用户 open_id，用于授权
    USER_OPEN_ID = "your_user_open_id"

    print("正在获取访问令牌...")
    token = get_tenant_access_token()
    print("令牌获取成功!\n")

    print("正在创建多维表格...")
    app_token, table_id = create_bitable(token)
    print()

    print("正在配置字段...")
    rename_first_field(token, app_token, table_id)
    add_fields(token, app_token, table_id)
    print()

    print("正在授权用户...")
    grant_user_access(token, app_token, USER_OPEN_ID)
    print("\n全部完成!")


if __name__ == "__main__":
    main()
