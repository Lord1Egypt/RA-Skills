from monitor import start_monitor

start_monitor(
    names=["平安银行", "贵州茅台"],
    interval=30,  # 30秒查一次
    threshold=1.5,  # 偏离1.5%触发
)
# print("run")
