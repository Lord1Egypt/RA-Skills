import os
import sys
import requests
import time
from feishu_docx_client import FeishuDocx

def main():
    app_id = "cli_a92c5076b7789cd2"
    app_secret = "9jPdCn49G54RFoEoDPUCVcptnWZnTZqp"
    folder_token = "CicIfQH2VlKqV0dBK4mceVMRnqf"
    
    file_path = "/Users/cpjhy0535/.openclaw/workspace-master/cases/空气炸锅鸡蛋饼 - 爆款拆解报告.md"
    file_name = "空气炸锅鸡蛋饼 - 爆款拆解报告(完美版)"
    
    if not os.path.exists(file_path):
        print(f"Error: File not found at {file_path}")
        sys.exit(1)
    
    client = FeishuDocx(app_id, app_secret)
    try:
        # 1. 上传文件到云端
        print(f"Uploading file: {file_path}")
        file_token = client.upload_file(file_path, folder_token)
        print(f"File uploaded, token: {file_token}")
        
        # 2. 发起导入任务 (Markdown -> Docx)
        print("Starting import task...")
        doc_token = client.import_markdown(file_token, file_name, folder_token)
        print(f"Import successful! New Doc Token: {doc_token}")
        print(f"URL: https://txx-claw.feishu.cn/docx/{doc_token}")
        
        # 3. 清理暂存的源文件
        print(f"Deleting temporary source file: {file_token}")
        client.delete_file(file_token)
        print("Cleanup successful.")
    except Exception as e:
        print(f"Error details: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
