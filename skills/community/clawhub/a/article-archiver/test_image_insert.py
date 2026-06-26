import requests
import json

# 飞书配置
APP_ID = "cli_a90ecd03bc399bcb"
APP_SECRET = "gdEsio0WzDtHEhHFeLS55wBseDpExVtg"
DOC_TOKEN = "FFvZdTzaxooPYPxZ4dhck9MYnFh"

# 获取 token
auth_url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
auth_response = requests.post(auth_url, json={"app_id": APP_ID, "app_secret": APP_SECRET})
token = auth_response.json()["tenant_access_token"]

# 读取图片 tokens
with open('/tmp/image_tokens.json', 'r') as f:
    image_tokens = json.load(f)

print(f"Image tokens: {image_tokens}")

# 获取文档所有 blocks
headers = {"Authorization": f"Bearer {token}"}
list_url = f"https://open.feishu.cn/open-apis/docx/v1/documents/{DOC_TOKEN}/blocks"
response = requests.get(list_url, headers=headers, params={"page_size": 500})

if response.status_code == 200:
    result = response.json()
    blocks = result['data']['items']
    print(f"\nTotal blocks: {len(blocks)}")
    
    # 找到第一个文本块（在元数据之后）
    target_block_id = None
    for i, block in enumerate(blocks):
        if block['block_type'] == 1:  # Text block
            print(f"Block {i}: {block['block_id']} - {block.get('text', {}).get('elements', [{}])[0].get('text_run', {}).get('content', '')[:50]}")
            if i > 5:  # 跳过前面的元数据块
                target_block_id = block['block_id']
                break
    
    if target_block_id:
        print(f"\nTarget block for image insertion: {target_block_id}")
        
        # 在这个块之后插入第一张图片
        create_url = f"https://open.feishu.cn/open-apis/docx/v1/documents/{DOC_TOKEN}/blocks/{target_block_id}/children"
        
        image_data = {
            "children": [
                {
                    "block_type": 27,  # Image block type
                    "image": {
                        "token": image_tokens[0]
                    }
                }
            ]
        }
        
        print(f"\nInserting image: {json.dumps(image_data, indent=2)}")
        
        insert_response = requests.post(create_url, headers=headers, json=image_data)
        print(f"\nInsert response: {insert_response.status_code}")
        print(json.dumps(insert_response.json(), indent=2, ensure_ascii=False))
else:
    print(f"Error: {response.status_code}")
    print(response.text)

