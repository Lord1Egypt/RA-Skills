import argparse
import sys
import os

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

from rich.console import Console
from rich.table import Table

from db import init_db, add_receipt, get_budget, set_budget, get_total_spent, get_receipts
from styling import print_banner, print_section, print_success, print_error, print_warning, print_info, print_key_value, COLORS

def main():
    init_db()
    parser = argparse.ArgumentParser(description="ClawReceipt 🧾 - ตัวช่วยจัดการใบเสร็จ (รับข้อมูลจาก OpenClaw)")
    
    subparsers = parser.add_subparsers(dest="command", help="คำสั่งที่ใช้งานได้")

    # Command: add
    parser_add = subparsers.add_parser("add", help="เพิ่มใบเสร็จใหม่ (สำหรับ OpenClaw 调用)")
    parser_add.add_argument("--date", required=True, help="วันที่ตัวอย่างเช่น 2026-02-27")
    parser_add.add_argument("--time", required=False, default="", help="เวลาตัวอย่างเช่น 15:30:00")
    parser_add.add_argument("--store", required=True, help="ชื่อร้านค้า")
    parser_add.add_argument("--amount", required=True, type=float, help="ราคารวม")
    parser_add.add_argument("--category", required=True, help="หมวดหมู่เช่น อาหาร, เดินทาง")

    # Command: tui
    parser_tui = subparsers.add_parser("tui", help="เปิดดูข้อมูลทั้งหมดผ่านหน้าจอ TUI แบบสวยงาม")

    # Command: budget
    parser_budget = subparsers.add_parser("budget", help="จัดการหรือตรวจสอบ Budget")
    parser_budget.add_argument("--set", type=float, help="ตั้งค่า Budget รายเดือน")

    # Command: alert
    parser_alert = subparsers.add_parser("alert", help="ตรวจสอบว่ายอดตอนนี้เกิน Budget หรือยัง (ใช้สำหรับเช็คสถานะเงียบๆ)")

    # Command: list
    parser_list = subparsers.add_parser("list", help="แสดงรายการใบเสร็จทั้งหมดในรูปแบบตาราง CLI")

    args = parser.parse_args()
    console = Console()

    if args.command == "add":
        print_banner("บันทึกใบเสร็จใหม่เข้าสู่ระบบ")
        add_receipt(args.date, args.time, args.store, args.amount, args.category)
        
        print_section("Processing Receipt")
        print_success("Saved perfectly! 🚀")
        print_key_value("Store", args.store)
        print_key_value("Amount", f"{args.amount:,.2f} ฿")
        print_key_value("Category", args.category)
        
        # ตรวจสอบ Budget ในตัว
        budget = get_budget()
        spent = get_total_spent()
        if budget > 0 and spent > budget:
            console.print()
            print_error(f"ALERT! Spent ({spent:,.2f} ฿) exceeds Monthly Budget ({budget:,.2f} ฿) 📉")

    elif args.command == "tui":
        # Import ตรงนี้เพื่อไม่ให้หน่วงเวลาตอนรัน CLI ปกติ
        from tui import ClawReceiptTUI
        app = ClawReceiptTUI()
        app.run()

    elif args.command == "budget":
        print_banner("Budget Management")
        if args.set is not None:
            set_budget(args.set)
            print_section("Update Success")
            print_success(f"New monthly budget is set to [bold {COLORS['warning']}]{args.set:,.2f} ฿[/]!")
        else:
            budget = get_budget()
            spent = get_total_spent()
            print_section("Status")
            print_key_value("Total Spent", f"[bold {COLORS['warning']}]{spent:,.2f} ฿[/]")
            print_key_value("Target Budget", f"[bold cyan]{budget:,.2f} ฿[/]")
            
            if budget > 0 and spent > budget:
                print_error("Exceeded Budget! Watch out!")
            else:
                print_success("Still within budget margin. Great job!")

    elif args.command == "alert":
        budget = get_budget()
        spent = get_total_spent()
        if budget > 0 and spent > budget:
            console.print(f"[bold red]🚨 Exceeded Budget! Spent: {spent}[/bold red]")
            sys.exit(1)
        else:
            console.print(f"[green]✅ Within Budget[/green]")
            sys.exit(0)
            
    elif args.command == "list":
        print_banner("All Recorded Receipts")
        df = get_receipts()
        if df.empty:
            print_info("No receipts found in database yet.")
            return
            
        table = Table(title="🧾 Receipt Archive (ClawReceipt)", 
                      title_style=f"bold {COLORS['primary']}",
                      header_style=f"bold {COLORS['info']}",
                      border_style=COLORS['gray'])
        table.add_column("ID", style=COLORS['gray'])
        table.add_column("Date", style="cyan")
        table.add_column("Time", style="blue")
        table.add_column("Store", style="magenta")
        table.add_column("Amount", justify="right", style=COLORS['warning'])
        table.add_column("Category", style=COLORS['success'])
        
        for index, row in df.iterrows():
            table.add_row(
                str(row['id']), 
                row['date'], 
                row['time'],
                row['store'], 
                f"{row['amount']:,.2f}", 
                row['category']
            )
            
        console.print(table)

    else:
        parser.print_help()

if __name__ == "__main__":
    main()
