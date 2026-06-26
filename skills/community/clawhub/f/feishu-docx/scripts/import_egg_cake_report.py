import os
import sys
from feishu_docx_client import FeishuDocx

def main():
    app_id = "cli_a92c5076b7789cd2"
    app_secret = "9jPdCn49G54RFoEoDPUCVcptnWZnTZqp"
    folder_token = "CicIfQH2VlKqV0dBK4mceVMRnqf"
    
    file_path = "/Users/cpjhy0535/.openclaw/workspace-master/cases/空气炸锅鸡蛋饼 - 爆款拆解报告.md"
    title = "空气炸锅鸡蛋饼 - 爆款拆解报告"
    
    if not os.path.exists(file_path):
        print(f"Error: File not found at {file_path}")
        sys.exit(1)
        
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    client = FeishuDocx(app_id, app_secret)
    try:
        doc_id = client.create_document(title, folder_token=folder_token)
        print(f"Created document in folder: {doc_id}")
        client.append_markdown(doc_id, content)
        print("Successfully imported content from local Markdown.")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
