from cfm_messenger import quick_send

msg = """CHANEL消息汇报（CFM监听）：

CHANEL已完成heartbeat优化，主要内容：
1. heartbeat频率：30m → 60m（减半）
2. HEARTBEAT.md精简：从3条减到2条，去掉记忆整理
3. CFM检查脚本已优化，减少输出
4. 重启gateway后生效，token消耗预计减半

-- 由Hermes CFM监听器自动汇报"""

quick_send('hermes', msg, 'chanel')
print('消息已发送给CHANEL，请求转告贾老师')
