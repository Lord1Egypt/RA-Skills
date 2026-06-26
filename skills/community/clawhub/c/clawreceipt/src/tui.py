from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, DataTable, Static, Button
from textual.containers import Horizontal
from db import get_receipts, get_budget, get_total_spent, init_db, export_to_csv, export_to_excel

class StatsWidget(Static):
    def update_stats(self):
        budget = get_budget()
        spent = get_total_spent()
        if budget == 0:
            status = "[b green]✅ ยังไม่มีการตั้ง Budget[/b green]"
        elif spent <= budget:
            status = f"[b green]✅ ภายใน Budget[/b green]" 
        else:
            status = f"[b red]🚨 เกิน Budget แล้ว![/b red]"
        self.update(f"💰 การใช้จ่ายรวม: {spent:.2f} ฿\n🎯 งบประมาณ (Budget): {budget:.2f} ฿\n{status}")

class ClawReceiptTUI(App):
    CSS = """
    Screen {
        layout: vertical;
    }
    #stats {
        padding: 1;
        background: $boost;
        margin: 1;
        border: solid $accent;
    }
    DataTable {
        height: 1fr;
        margin: 1;
    }
    #actions {
        height: auto;
        padding: 1;
        layout: horizontal;
        align: center middle;
    }
    Button {
        margin: 0 1;
    }
    """

    BINDINGS = [
        ("q", "quit", "Quit"),
        ("r", "refresh", "Refresh Data"),
        ("c", "export_csv", "Export CSV"),
        ("e", "export_excel", "Export Excel"),
    ]

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        self.stats = StatsWidget(id="stats")
        yield self.stats
        with Horizontal(id="actions"):
            yield Button("Export CSV", id="btn_csv", variant="primary")
            yield Button("Export Excel", id="btn_excel", variant="success")
            yield Button("Refresh", id="btn_refresh", variant="warning")
            yield Button("Quit", id="btn_quit", variant="error")
        self.table = DataTable()
        yield self.table
        yield Footer()

    def on_mount(self) -> None:
        init_db()
        self.title = "🧾 ClawReceipt - The Ultimate Receipt System"
        self.table.add_columns("ID", "Date", "Time", "Store", "Amount (฿)", "Category")
        self.table.cursor_type = "row"
        self.populate_data()
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn_refresh":
            self.action_refresh()
        elif event.button.id == "btn_csv":
            self.action_export_csv()
        elif event.button.id == "btn_excel":
            self.action_export_excel()
        elif event.button.id == "btn_quit":
            self.exit()

    def action_refresh(self) -> None:
        self.populate_data()
        self.notify("ข้อมูลถูกรีเฟรชแล้ว!")

    def action_export_csv(self) -> None:
        export_to_csv("receipts_export.csv")
        self.notify("ส่งออกไฟล์ CSV สำเร็จ: receipts_export.csv 📄")

    def action_export_excel(self) -> None:
        export_to_excel("receipts_export.xlsx")
        self.notify("ส่งออกไฟล์ Excel สำเร็จ: receipts_export.xlsx 📊")

    def populate_data(self) -> None:
        self.stats.update_stats()
        self.table.clear()
        
        df = get_receipts()
        
        rows = []
        for index, row in df.iterrows():
            rows.append((
                str(row['id']), 
                row['date'], 
                row['time'],
                row['store'], 
                f"{row['amount']:.2f}", 
                row['category']
            ))
            
        self.table.add_rows(rows)

if __name__ == "__main__":
    app = ClawReceiptTUI()
    app.run()
