from binance_agent.agent import BinanceTradingAgent

if __name__ == "__main__":
    # เริ่มต้น Agent
    # หมายเหตุ: ต้องตั้งค่า API Key ใน binance_agent/config.py ก่อนใช้งานจริง
    agent = BinanceTradingAgent()
    
    # รัน Agent 1 รอบเพื่อทดสอบความถูกต้องของโมดูล (Dry Run)
    print("--- เริ่มการทดสอบ Agent (Dry Run) ---")
    agent.run_once()
    print("--- จบการทดสอบ ---")
    
    # หากต้องการรันแบบต่อเนื่อง ให้ใช้:
    # agent.start_loop(interval_seconds=3600) # รันทุก 1 ชั่วโมง
