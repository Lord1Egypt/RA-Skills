"""简单测试 Direct P2P 互通"""

import sys
import os
import logging
# 设置日志级别
logging.basicConfig(level=logging.DEBUG, format='%(levelname)s:%(name)s:%(message)s')

# 添加 workspace 根目录到 path
WORKSPACE = r"C:\Users\wang20\.openclaw\workspace"
if WORKSPACE not in sys.path:
    sys.path.insert(0, WORKSPACE)

from skills.clawphone.adapter.direct import DirectAdapter
from skills.clawphone.adapter.clawphone import ClawPhone
import time

print("=== 测试 Direct P2P ===\n")

# Alice
alice = ClawPhone()
alice._my_node_id = "ALICE"
alice_adapter = DirectAdapter("ALICE", listen_port=8766)
alice_addr = alice_adapter.start()   # 应该是同步返回字符串
alice.set_adapter(alice_adapter)
alice_num = alice.register("alice")
print(f"Alice: 号码={alice_num}, 地址={alice_addr}, type={type(alice_addr)}")

# Bob
bob = ClawPhone()
bob._my_node_id = "BOB"
bob_adapter = DirectAdapter("BOB", listen_port=8767)
bob_addr = bob_adapter.start()
print(f"[DEBUG] bob_adapter._address = {bob_adapter._address}")
bob.set_adapter(bob_adapter)
print(f"[DEBUG] bob._adapter is bob_adapter: {bob._adapter is bob_adapter}")
bob_num = bob.register("bob")
print(f"[DEBUG] bob._adapter.get_my_address() = {bob._adapter.get_my_address() if bob._adapter else 'None'}")
print(f"[DEBUG] after register, bob._adapter._address = {bob._adapter._address if bob._adapter else 'None'}")
print(f"Bob: 号码={bob_num}, 地址={bob_addr}, type={type(bob_addr)}\n")

# 绑定
alice.add_contact(alias="bob", phone_id=bob_num, address=bob_addr)
bob.add_contact(alias="alice", phone_id=alice_num, address=alice_addr)
print("[*] 绑定完成")

# 打印数据库内容（调试）
import sqlite3
db = sqlite3.connect(r"C:\Users\wang20\.openclaw\skills\clawphone\phonebook.db")
cur = db.cursor()
cur.execute("SELECT alias, phone_id, address FROM phones")
rows = cur.fetchall()
print("[DB] 当前记录:")
for r in rows:
    print(f"  alias={r[0]}, phone_id={r[1]}, address={r[2]}")
db.close()

# 回调
def on_msg(msg):
    print(f"[收到] {msg.get('from')}: {msg.get('content')}")

alice.on_message = on_msg
bob.on_message = on_msg

# 测试 Alice -> Bob
print("\n[测试] Alice 呼叫 Bob...")
try:
    ok = alice.call(bob_num, "Hello Bob!")
    print(f"  发送结果: {ok}, type: {type(ok)}")
except Exception as e:
    print(f"  异常: {e}")
import time; time.sleep(0.5)

# 测试 Bob -> Alice
print("[测试] Bob 呼叫 Alice...")
try:
    ok = bob.call(alice_num, "Hi Alice!")
    print(f"  发送结果: {ok}, type: {type(ok)}")
except Exception as e:
    print(f"  异常: {e}")
time.sleep(0.5)

# 清理
alice_adapter.stop()
bob_adapter.stop()
print("\n[完成]")
