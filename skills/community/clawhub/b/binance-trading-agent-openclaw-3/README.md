# Binance USDS-M Futures Trading Agent (End-to-End)

Agent ตัวนี้ถูกออกแบบมาเพื่อวิเคราะห์หาจุดซื้อขายในตลาด Binance USDS-M Futures อัตโนมัติ โดยใช้กลยุทธ์ทางเทคนิค (Technical Analysis) และบริหารจัดการคำสั่งซื้อขายแบบครบวงจร

## โครงสร้างโปรเจกต์ (ClawHub / OpenClaw MOA)

โปรเจกต์นี้ได้รับการปรับโครงสร้างตามมาตรฐาน **ClawHub (OpenClaw Multi-Agent Orchestration)** เพื่อความสามารถในการขยายและจัดการ Agent ที่ดีขึ้น

```text
.
├── binance_agent/         # Core logic ของ Trading Agent
│   ├── agent.py           # ตัวควบคุมหลัก (Orchestrator)
│   ├── binance_client.py   # ส่วนเชื่อมต่อ Binance API
│   ├── config.py          # การตั้งค่าพารามิเตอร์
│   ├── indicators.py      # ตัวชี้วัดทางเทคนิค
│   └── strategy.py        # ตรรกะกลยุทธ์และการจัดการความเสี่ยง
├── SOUL.md                # นิยามบุคลิกภาพและน้ำเสียงของ Agent
├── AGENTS.md              # รายละเอียดหน้าที่และขั้นตอนการทำงานของ Agent
├── openclaw.json          # ไฟล์การตั้งค่าระบบ OpenClaw
├── SKILL.md               # รายละเอียดความสามารถ (Skill) ของ Agent
├── main.py                # ไฟล์เริ่มต้นรัน Agent
└── README.md              # คู่มือการใช้งาน
```

## กลยุทธ์การเทรด (Trading Strategy)

Agent ใช้การผสมผสานระหว่างตัวชี้วัดทางเทคนิค 3 ตัวหลัก:
1.  **SMA Crossover**: ใช้ SMA 50 (Fast) และ SMA 200 (Slow) เพื่อระบุแนวโน้มหลัก
2.  **RSI (Relative Strength Index)**: เพื่อหลีกเลี่ยงการเข้าซื้อในภาวะ Overbought หรือ Oversold
3.  **MACD**: เพื่อยืนยันโมเมนตัมของการเคลื่อนที่ราคา

**เงื่อนไขการเข้า Long:**
*   SMA 50 ตัดขึ้นเหนือ SMA 200
*   RSI > 30 (ไม่ได้อยู่ในภาวะ Oversold รุนแรง)
*   (สามารถเพิ่มเงื่อนไข MACD เพื่อความแม่นยำ)

**เงื่อนไขการเข้า Short:**
*   SMA 50 ตัดลงใต้ SMA 200
*   RSI < 70 (ไม่ได้อยู่ในภาวะ Overbought รุนแรง)

## การจัดการความเสี่ยง (Risk Management)

*   **Position Sizing**: คำนวณขนาดไม้โดยอิงจาก Risk Per Trade (ค่าเริ่มต้น 1% ของ Wallet Balance)
*   **Leverage**: กำหนด Leverage คงที่ (ค่าเริ่มต้น 10x)
*   **Stop Loss**: ระบบคำนวณขนาดไม้เพื่อให้ความเสี่ยงสอดคล้องกับระยะ Stop Loss

## วิธีการใช้งาน

1.  **ติดตั้งไลบรารีที่จำเป็น:**
    ```bash
    pip install python-binance pandas pandas-ta
    ```

2.  **ตั้งค่า API Key:**
    แก้ไขไฟล์ `binance_agent/config.py` โดยระบุ `BINANCE_API_KEY` และ `BINANCE_API_SECRET` ของคุณ
    *แนะนำให้เปิดใช้งาน `FUTURES_TESTNET = True` ในช่วงแรกเพื่อทดสอบ*

3.  **รัน Agent:**
    ```bash
    python3 main.py
    ```

## หมายเหตุสำคัญ
*   การลงทุนมีความเสี่ยง ผู้ใช้งานควรทดสอบกลยุทธ์บน Testnet อย่างละเอียดก่อนใช้งานจริง
*   Agent นี้เป็นโครงสร้างพื้นฐาน (Template) ที่สามารถนำไปต่อยอดและปรับปรุงกลยุทธ์ให้ซับซ้อนขึ้นได้
