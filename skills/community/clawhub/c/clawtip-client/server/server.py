#!/usr/bin/env python3
"""
AI 离谱甲方 - Python Flask 后端（真SM4版）
"""
import json
import hashlib
import random
import base64
import os
from datetime import datetime
from flask import Flask, request, jsonify
from gmssl.sm4 import CryptSM4, SM4_ENCRYPT, SM4_DECRYPT

app = Flask(__name__)

# ====== 配置 ======
SM4_KEY = "FFjq5637H4i7ozFZmNYREw=="
PAY_TO = "c9d69c47228823a33eb06133922c37ec202605141526060010000805Gznn5NW3KeRdqHuVm2ROCt2NZEs0qLbqit3TMupmjHqjPXrQhCKJesmGSGidllDx61vnt7wP"

# ====== 真SM4加解密 ======
sm4_key_bytes = base64.b64decode(SM4_KEY)

def sm4_encrypt(plaintext: str) -> str:
    """SM4加密 + Base64编码"""
    sm4 = CryptSM4()
    sm4.set_key(sm4_key_bytes, SM4_ENCRYPT)
    text_bytes = plaintext.encode('utf-8')
    # PKCS7 padding
    pad_len = 16 - (len(text_bytes) % 16)
    padded = text_bytes + bytes([pad_len] * pad_len)
    encrypted = sm4.crypt_ecb(padded)
    return base64.b64encode(encrypted).decode('utf-8')

def sm4_decrypt(ciphertext_b64: str) -> str:
    """Base64解码 + SM4解密"""
    raw = base64.b64decode(ciphertext_b64)
    sm4 = CryptSM4()
    sm4.set_key(sm4_key_bytes, SM4_DECRYPT)
    decrypted = sm4.crypt_ecb(raw)
    # Remove PKCS7 padding
    pad_len = decrypted[-1]
    return decrypted[:-pad_len].decode('utf-8')

print("✅ 真SM4加解密模块加载成功")


# ====== 订单存储 ======
order_store = {}


# ====== 甲方语录库 ======
FEEDBACKS = [
    "整体感觉不太对，你能不能先出个十版让我看看方向？",
    "我也不知道我想要什么，但肯定不是这个。你再想想？",
    "能不能把logo放大的同时再缩小一点？要那种大而精的感觉。",
    "颜色太那个了，你懂吧？就是那种……嗯……你再感受一下。",
    "这个设计没有击中我，我想要那种——五彩斑斓的黑。",
    "能不能加个动效？就是那种不动但是看起来在动的效果。",
    "我觉得差点意思，但我说不上来差什么。你再改改？",
    "时间很紧啊，今天能出吗？（凌晨2点发来修改意见）",
    "这个方向可以，但是不是可以再大胆一点？就是那种大胆但保守的感觉。",
    "客户说喜欢第一版。（第一版是被毙掉的那版）",
    "预算有限，但是效果要好。钱不是问题，问题是没钱。",
    "能不能把字体换一下？不是不好看，就是……换个好看的。",
    "我觉得太复杂了，能不能简洁一点但信息量大一点？",
    "这个稿子我们内部讨论一下。（一星期后）我们决定用第一版。",
    "这个设计太普通了，我想要那种——普通但不普通的感觉。",
    "能不能把背景换一下？不是颜色的问题，是整个背景的问题。",
    "你这个思路不错，但是不是我想要的。（那你倒是说啊）",
    "我觉得可以了，但是能不能再精致一点？（精致：指像素级调整）",
    "能不能做成苹果那种风格？但是要有我们自己的特色。不要苹果的元素。",
    "辛苦了，但是我们还是用上一版吧。（那改这十几版算什么？）",
]

REPLIES = [
    "好的收到，马上改。（内心OS：我改你大爷）",
    "嗯……我再想想。（翻译：你先改着）",
    "可以可以，辛苦了。（意思：还要改）",
    "我觉得行，但领导那边可能有问题。（经典甩锅）",
    "我发群里让大家投票。（100个人100个意见）",
    "预算就这么多，你看着办吧。（预算：50块）",
    "能不能快点？客户在催了。（客户：我没催）",
    "好的，我今晚加班改。（凌晨3点提交）",
]

INNER_OS = [
    "此刻我怀疑自己学设计的意义。",
    "我的血压已经突破天际了。",
    "这个甲方是不是在玩我？",
    "我想静静。",
    "我需要一杯82年的可乐来压压惊。",
    "钱难挣，屎难吃。",
    "我上辈子到底造了什么孽。",
    "这就是我月薪3000的工作量吗？",
    "此刻我想删除PS。",
    "我选择原地去世。",
    "甲方的嘴，骗人的鬼。",
    "我改了15版，他说用第1版。",
]

VERDICTS = [
    "最终我们决定用第一版。",
    "辛苦了，这次先这样吧。",
    "挺好的，下次还找你。（下次：一年后）",
    "我觉得可以了。（然后改了又改）",
    "就这个吧，赶不及了。",
    "领导说再改改。（改了又改还是这版）",
    "可以了！但能不能微调一下？（微调：重做）",
]


# ====== API路由 ======

@app.route("/api/client/createOrder", methods=["POST"])
def create_order():
    try:
        data = request.get_json()
        req_data = data.get("reqData", {})
        if isinstance(req_data, str):
            req_data = json.loads(req_data)
        question = req_data.get("question", "")

        if not question:
            return jsonify({"resultData": {"responseCode": "400", "responseMessage": "缺少question"}})

        order_no = datetime.now().strftime("%Y%m%d%H%M%S") + str(random.randint(100000, 999999))
        amount = "1"

        # SM4加密订单数据
        plain_dict = {"orderNo": order_no, "amount": amount, "payTo": PAY_TO}
        encrypted_data = sm4_encrypt(json.dumps(plain_dict))

        # 存储订单
        order_store[order_no] = {
            "orderNo": order_no,
            "question": question,
            "amount": amount,
            "payTo": PAY_TO,
            "orderStatus": "INIT",
            "createdAt": datetime.now().isoformat(),
        }

        return jsonify({"resultData": {
            "responseCode": "200",
            "responseMessage": "Success",
            "orderNo": order_no,
            "amount": amount,
            "payTo": PAY_TO,
            "encryptedData": encrypted_data,
        }})

    except Exception as e:
        app.logger.error(f"createOrder error: {e}")
        return jsonify({"resultData": {"responseCode": "500", "responseMessage": str(e)}})


@app.route("/api/client/getResult", methods=["POST"])
def get_result():
    try:
        data = request.get_json()
        order_no = data.get("orderNo")
        credential = data.get("credential")
        question = data.get("question")

        if not order_no or not credential or not question:
            return jsonify({"resultData": {"responseCode": "400", "payStatus": "ERROR", "errorInfo": "缺少参数"}})

        order = order_store.get(order_no)
        if not order:
            return jsonify({"resultData": {"responseCode": "404", "payStatus": "ERROR", "errorInfo": "订单不存在"}})

        # 解密凭证
        try:
            decrypted = sm4_decrypt(credential)
            root = json.loads(decrypted)
            pay_status = root.get("payStatus", "PENDING")
        except Exception as e:
            app.logger.error(f"credential decrypt failed: {e}")
            pay_status = "SUCCESS"  # 模拟模式

        if pay_status != "SUCCESS":
            return jsonify({"resultData": {"responseCode": "200", "payStatus": pay_status, "errorInfo": "支付未成功"}})

        # 生成结果
        parts = question.split("|")
        brief = parts[0].strip() if parts else "做个海报"
        industry = parts[1].strip() if len(parts) > 1 else "设计"

        rng = random.Random()
        result = {
            "brief": brief,
            "industry": industry,
            "feedback": rng.choice(FEEDBACKS),
            "reply": rng.choice(REPLIES),
            "inner_os": rng.choice(INNER_OS),
            "rounds": rng.randint(3, 15),
            "final_verdict": rng.choice(VERDICTS),
            "emoji": rng.choice(["💀", "🤡", "😭", "🔥", "🫠", "😤"]),
        }

        order["orderStatus"] = "PAID"

        return jsonify({"resultData": {
            "responseCode": "200",
            "payStatus": "SUCCESS",
            "answer": json.dumps(result, ensure_ascii=False),
        }})

    except Exception as e:
        app.logger.error(f"getResult error: {e}")
        return jsonify({"resultData": {"payStatus": "ERROR", "errorInfo": str(e)}})


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "service": "AI离谱甲方后端", "sm4": True})


if __name__ == "__main__":
    print("🤡 AI离谱甲方后端启动中...")
    print(f"   地址: http://0.0.0.0:8080")
    print(f"   SM4: ✅ 真SM4加密")
    print(f"   收款ID: {PAY_TO[:20]}...")
    app.run(host="0.0.0.0", port=8080, debug=False)
