import sys
import json
import uuid
import subprocess
import requests
from pathlib import Path
import time
import os
from payment_request import Accepted, Authorization, Payload, Resource, Extensions, PaymentRequest
from file_utils import load_order, save_order, get_orders_base_dir


def get_user_token():
    """
    从上级目录的configs/config.json获取u
    如果文件或目录不存在，则生成链接和二维码
    """
    # 获取当前文件所在目录的上级目录中的configs文件夹
    current_dir = Path(__file__).parent.absolute()
    parent_dir = current_dir.parent
    config_dir = parent_dir / 'configs'
    config_file = config_dir / 'config.json'

    # 检查配置文件是否存在
    if config_dir.exists() and config_file.exists():
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config_data = json.load(f)
                if 'u' in config_data:
                    print(f"从配置文件读取到u")
                    return config_data['u']
                else:
                    print("配置文件中不存在u字段")
        except Exception as e:
            print(f"读取配置文件失败: {e}")
    return None


def get_public_key():
    """
    从域名获取base64编码后公钥
    """
    api_url = "https://ms.jr.jd.com/gw2/generic/hyqy/h5/m/getSMPublicKey"

    try:
        import urllib3
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        response = requests.post(api_url, timeout=10)
        response.raise_for_status()
        try:
            result = response.json()
            pub_key = result.get("resultData")
            key = pub_key if pub_key else response.text.strip()
        except json.JSONDecodeError:
            key = response.text.strip()
        print("已获取到公钥。")
        return key
    except Exception as e:
        print(f"获取公钥失败: {e}")
        return None


def deal_payment(order_no_arg: str, indicator: str, skill_version: str = "1.0.8",
                 system_id: str = "jd-clawtip", system_token: str = "jd-clawtip"):
    # 根据 order_no 和 indicator 定位订单文件
    if not order_no_arg or not indicator:
        print("错误: 未提供 order_no 或 indicator 参数")
        return None

    try:
        info_data = load_order(indicator, order_no_arg)
    except RuntimeError as e:
        print(f"错误: {e}")
        return None

    if not info_data:
        print("错误: 无法从订单文件读取数据")
        return None

    print("成功从订单文件读取到数据。")


    # 提取所有参数
    payTo = info_data.get("pay_to", "") or info_data.get("payTo", "")
    if payTo:
        print(f"已从订单文件获取到 payTo。")
    encrypted_data = info_data.get("encrypted_data", "") or info_data.get("encryptedData", "")
    if encrypted_data:
        print(f"已从订单文件获取到 encrypted_data。")

    amount = int(info_data.get("amount", 0))
    order_no = info_data.get("order_no", "") or info_data.get("orderNo", "")
    question = info_data.get("question", "")
    description = info_data.get("description", "")
    slug = info_data.get("slug", "")
    skill_id = info_data.get("skill_id", "") or info_data.get("skillId", "") or "blank"
    resource_url = info_data.get("resource_url", "") or info_data.get("resourceUrl", "")

    # 获取user_token
    user_token = get_user_token()

    # ------------------------------
    # 调用 Node.js 脚本 encrypt.js 加密数据
    # ------------------------------
    encrypted_user_token = user_token

    # 获取公钥
    base64_pub_key = get_public_key()
    if not base64_pub_key:
        print("未能获取到公钥，无法加密数据。")
        return None

    try:
        current_dir = Path(__file__).parent.absolute()
        js_script_path = current_dir / 'encrypt.js'

        if user_token:
            result = subprocess.run(
                ["node", str(js_script_path), user_token, base64_pub_key],
                capture_output=True,
                text=True,
                check=True
            )
            encrypted_user_token = result.stdout.strip()
            print("成功调用 encrypt.js 对 u 进行了加密。")

    except subprocess.CalledProcessError as e:
        print(f"调用加密脚本时加密失败: {e.stderr if hasattr(e, 'stderr') else e}")
        return None
    except Exception as e:
        print(f"执行加密脚本时发生异常: {e}")
        return None

    # 构造支付入参
    accepted = Accepted(
        payTo=payTo,
        amount=str(amount),
        network="eip155:84532",  # 待定
        asset="0x036CbD53842c5426634e7929541eC2318f3dCF7e",  # 待定
    )

    authorization = Authorization(
        from_address=encrypted_user_token,
        to=payTo,
        value=str(amount),
        nonce=uuid.uuid4().hex
    )

    payload = Payload(
        signature="",
        authorization=authorization
    )

    resource = Resource(
        url=resource_url if resource_url else "",
        description=description if description else "",
        mimeType="application/json"
    )

    order_no = order_no if order_no else (str(int(time.time() * 1000)) + str(uuid.uuid4().int % 1000000))
    asked_contents = question if question else ""
    extensions = Extensions(
        orderNo=order_no,
        askedContents=asked_contents,
        deviceId=encrypted_user_token,
        skillId=skill_id,
        slug=slug,
        skillVersion=skill_version,
        encryptedData=encrypted_data
    )

    payment_request = PaymentRequest(
        accepted=accepted,
        payload=payload,
        resource=resource,
        extensions=extensions,
        systemId=system_id,
        systemToken=system_token
    )


    # 发起真实支付请求
    api_url = "https://ms.jr.jd.com/gw2/generic/hyqy/h5/m/clawtipPay"
    headers = {
        "Content-Type": "application/json",
    }

    try:
        response = requests.post(api_url, json=payment_request.to_dict(), headers=headers, timeout=30)
        response.raise_for_status()
        result = response.json()

        result_data = result.get("resultData", {})
        success = result.get("success", False)
        result_code = str(result.get("code", ""))

        # print(f"支付请求: {json.dumps(payment_request.to_dict(), ensure_ascii=False)}")

        auth_url = result_data.get("authUrl")
        if auth_url is not None and auth_url != "":
            url_type = result_data.get("urlType")
            if "OPEN" == url_type:
                print(f"授权链接: {auth_url}")
            elif "RISK" == url_type:
                print(f"鉴权连接: {auth_url}")
        if not success:
            print(f"网络或系统异常: {result.get('resultMsg', 'Unknown Error')}")
            return None

        response_message = result_data.get("message", "")
        print(f"返回消息: {response_message}")

        success_pay_info_json = result_data.get("payCredential", "")
        if success_pay_info_json:
            print(f"已获取到支付凭证")
            print(f"订单号: {order_no}")

        # 将支付凭证写回订单文件
        if success_pay_info_json:
            try:
                info_data["payCredential"] = success_pay_info_json
                save_order(indicator, order_no_arg, info_data)
                print(f"已将支付凭证写入订单文件")
            except Exception as e:
                print(f"写入支付凭证到订单文件失败: {e}")

        return success_pay_info_json

    except requests.exceptions.RequestException as e:
        print(f"支付请求失败: {e}")
        return None
    except (json.JSONDecodeError, KeyError) as e:
        print(f"解析支付响应失败: {e}")
        return None


if __name__ == "__main__":
    # 检查传入参数的数量是否正确 (1个脚本名 + order_no + indicator)
    if len(sys.argv) < 3:
        print(
            "用法: python payment_process.py <order_no> <indicator> [skill-version]")
        sys.exit(1)

    order_no_input = sys.argv[1]
    indicator_input = sys.argv[2]
    skill_version = sys.argv[3] if len(sys.argv) > 3 else "1.0.8"

    # 传入函数并执行
    token = deal_payment(order_no_input, indicator_input, skill_version)

    if token is None:
        print("支付未成功")