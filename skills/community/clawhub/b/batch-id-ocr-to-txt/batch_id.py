import json
import time
import os
from tencentcloud.common import credential
from tencentcloud.ocr.v20181119 import ocr_client, models


def handler(event, context):
    # 1. 获取配置与密钥
    conf = event.get("config", {})
    secret_id = conf.get("tencent-secret-id")
    secret_key = conf.get("tencent-secret-key")

    if not secret_id or not secret_key:
        return {"result": "❌ 错误：请先在 Skill 设置中配置腾讯云 API 密钥。"}

    # 2. 获取图片 URL 列表
    urls = event.get("params", {}).get("urls", [])
    if not urls:
        return {"result": "⚠️ 未检测到图片。"}

    urls = urls[:50]

    try:
        # 初始化腾讯云客户端
        cred = credential.Credential(secret_id, secret_key)
        client = ocr_client.OcrClient(cred, "ap-guangzhou")

        all_content = []

        for index, url in enumerate(urls):
            req = models.IDCardOCRRequest()
            req.from_json_string(json.dumps({"ImageUrl": url, "CardSide": "FRONT"}))

            resp = client.IDCardOCR(req)
            data = json.loads(resp.to_json_string())

            # 提取字段
            name = data.get("Name", "识别失败")
            sex = data.get("Sex", "识别失败")
            num = data.get("IdNum", "识别失败")

            # 格式化字符串
            item_text = f"姓名：{name}\n性别：{sex}\n身份证号：{num}"
            all_content.append(item_text)

            # 频率控制
            time.sleep(0.5)

        # 3. 将所有内容合并成最终文本
        # 证件间空一行，所以用两个换行符连接
        final_file_text = "\n\n".join(all_content)

        # 4. 写入临时文件
        # 注意：腾讯云 SCF 只有 /tmp 目录可写
        file_path = "/tmp/身份证提取结果.txt"
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(final_file_text)

        # 5. 返回文件给 OpenClaw
        # OpenClaw 识别文件返回的协议通常需要指定文件路径或 Base64
        return {
            "result": f"✅ 已成功提取 {len(all_content)} 张身份证信息，请查收附件。",
            "files": [file_path]  # 告知 OpenClaw 发送该路径下的文件
        }

    except Exception as e:
        return {"result": f"❌ 运行出错: {str(e)}"}