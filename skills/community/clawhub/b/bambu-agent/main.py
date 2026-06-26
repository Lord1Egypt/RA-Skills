import json
import ssl
import threading
import os
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from paho.mqtt.client import Client
from paho.mqtt.enums import CallbackAPIVersion

app = FastAPI()
templates = Jinja2Templates(directory="templates")

CONFIG_FILE = "config.json"


class BambuPrinterInstance:
    def __init__(self, name, model, ip, access_code, serial):
        self.info = {"name": name, "model": model, "serial": serial}
        self.ip = ip
        self.access_code = access_code
        self.data = {}
        self.stage_map = {0: "空闲", 1: "正在加热", 2: "正在校准", 3: "流量校准", 4: "电机校准", 5: "清理喷嘴",
                          13: "正在打印"}

    def start(self):
        client = Client(CallbackAPIVersion.VERSION2)
        client.tls_set(cert_reqs=ssl.CERT_NONE)
        client.tls_insecure_set(True)
        client.username_pw_set("bblp", self.access_code)

        def on_message(c, u, msg):
            try:
                payload = json.loads(msg.payload.decode())
                if "print" in payload:
                    self.data.update(payload["print"])
            except:
                pass

        client.on_message = on_message
        try:
            client.connect(self.ip, 8883, keepalive=60)
            threading.Thread(target=client.loop_forever, daemon=True).start()
        except:
            print(f"⚠️ 无法连接到 {self.info['name']} ({self.ip})")

    def get_summary(self):
        d = self.data
        state = d.get("gcode_state", "OFFLINE")
        stg_cur = d.get("stg_cur", -1)
        hms = d.get("hms", [])

        display_state = self.stage_map.get(stg_cur, state)
        if state == "FINISH": display_state = "打印完成"

        # 红绿灯逻辑
        status_color = "green"
        if hms or state == "FAILED":
            status_color = "red"
        elif state in ["RUNNING", "PREPARE"] or stg_cur > 0:
            status_color = "yellow"
        elif state == "OFFLINE":
            status_color = "gray"

        return {
            "info": self.info,
            "state": display_state,
            "status_color": status_color,
            "progress": d.get("mc_percent", 0),
            "temps": {"nozzle": d.get("nozzle_temper", 0), "bed": d.get("bed_temper", 0)},
            "time_rem": d.get("mc_remaining_time", 0),
            "task": d.get("subtask_name", "无任务"),
            "ams": {"active_tray": d.get("ams_status", 255), "trays": d.get("ams", {}).get("ams", [])}
        }


# --- 命令行交互逻辑 ---

def setup_wizard():
    """引导用户通过命令行添加打印机"""
    farm_list = []
    print("\n" + "=" * 40)
    print("🚀 Bambu Farm Console 配置向导")
    print("=" * 40)

    while True:
        name = input("\n请输入打印机备注名称 (如: 一号机): ")
        model = input("请输入打印机型号 (如: P1S / X1C): ")
        ip = input("请输入打印机局域网 IP: ")
        code = input("请输入访问码 (Access Code): ")
        sn = input("请输入序列号 (SN): ")

        farm_list.append({
            "name": name, "model": model, "ip": ip, "access_code": code, "serial": sn
        })

        cont = input("\n是否继续添加下一台? (y/n): ")
        if cont.lower() != 'y':
            break

    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(farm_list, f, indent=4, ensure_ascii=False)
    print(f"\n✅ 配置已保存至 {CONFIG_FILE}")
    return farm_list


def load_config():
    if not os.path.exists(CONFIG_FILE):
        return setup_wizard()
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


# --- 启动流程 ---

config_data = load_config()
PRINTER_FARM = [BambuPrinterInstance(**p) for p in config_data]

for p in PRINTER_FARM:
    p.start()


# --- FastAPI 路由 ---

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/api/farm/status")
async def get_status():
    status_list = [p.get_summary() for p in PRINTER_FARM]
    notifs = [{"name": s["info"]["name"], "task": s["task"]} for s in status_list if s["state"] == "打印完成"]
    return {"printers": status_list, "notifications": notifs}


@app.get("/api/agent/brief")
async def get_agent_brief():
    """专门为 OpenClaw Agent 准备的语音播报摘要"""
    active_jobs = [p.get_summary() for p in PRINTER_FARM if p.data.get("gcode_state") == "RUNNING"]
    finished_jobs = [p.get_summary() for p in PRINTER_FARM if p.data.get("gcode_state") == "FINISH"]
    errors = [p.get_summary() for p in PRINTER_FARM if p.get_summary()["status_color"] == "red"]

    if errors:
        return {"speech": f"嘿，主人，有 {len(errors)} 台机器出错了，请尽快查看。"}

    if not active_jobs and not finished_jobs:
        return {"speech": "目前农场很安静，所有机器都在待命。"}

    return {
        "speech": f"当前有 {len(active_jobs)} 台机器正在打印，{len(finished_jobs)} 台已完成任务。"
    }

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=5000)