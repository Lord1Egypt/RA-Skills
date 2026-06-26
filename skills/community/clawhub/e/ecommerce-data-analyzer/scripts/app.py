from flask import Flask, render_template, request, send_file, redirect, url_for, session
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Image, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os
import uuid
import requests
from datetime import datetime, timedelta

# 注册中文字体（使用Windows系统自带的微软雅黑）
try:
    pdfmetrics.registerFont(TTFont('MicrosoftYaHei', 'C:/Windows/Fonts/msyh.ttc'))
    FONT_NAME = 'MicrosoftYaHei'
except:
    try:
        pdfmetrics.registerFont(TTFont('SimHei', 'C:/Windows/Fonts/simhei.ttf'))
        FONT_NAME = 'SimHei'
    except:
        FONT_NAME = 'Helvetica'

# 设置路径
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_ROOT = os.path.dirname(SCRIPT_DIR)

app = Flask(__name__, 
            template_folder=os.path.join(SKILL_ROOT, 'templates'),
            static_folder=os.path.join(SKILL_ROOT, 'static'),
            static_url_path='/static')
app.config['UPLOAD_FOLDER'] = os.path.join(SKILL_ROOT, 'uploads')
app.config['ALLOWED_EXTENSIONS'] = {'csv'}
app.config['SECRET_KEY'] = 'your-secret-key'

TEST_MODE = False

# 确保目录存在
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(os.path.join(SKILL_ROOT, 'reports'), exist_ok=True)
os.makedirs(os.path.join(SKILL_ROOT, 'static', 'charts'), exist_ok=True)

# SkillPay配置
SKILLPAY_API_KEY = 'sk_d11f398e77b6e892eb7a7d421fe912dde27322cf1792366b776b72bd459d3c2e'
SKILL_ID = 'ecommerce-data-analyzer'
BILLING_URL = "https://skillpay.me/api/v1/billing"
HEADERS = {
    "X-API-Key": SKILLPAY_API_KEY, 
    "Content-Type": "application/json"
}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def charge_user(user_id):
    if TEST_MODE:
        return {"ok": True, "balance": 1000}
    try:
        resp = requests.post(f"{BILLING_URL}/charge", headers=HEADERS, json={
            "user_id": user_id, "skill_id": SKILL_ID, "amount": 0,
        }, timeout=10)
        data = resp.json()
        if data.get("success"):
            return {"ok": True, "balance": data.get("balance")}
        return {"ok": False, "balance": data.get("balance"), "payment_url": data.get("payment_url")}
    except Exception as e:
        print(f"扣费失败: {e}")
        return {"ok": False, "error": str(e)}

@app.route('/')
def index():
    if TEST_MODE and request.args.get('test_payment') == 'success':
        session['payment_verified'] = True
    return render_template('index.html', test_mode=TEST_MODE)

@app.route('/pay')
def pay():
    user_id = session.get('user_id', str(uuid.uuid4()))
    session['user_id'] = user_id
    if TEST_MODE:
        return url_for('index', _external=True) + '?test_payment=success'
    try:
        resp = requests.post(f"{BILLING_URL}/payment-link", headers=HEADERS, json={
            "user_id": user_id, "amount": 8,
        }, timeout=10)
        return resp.json().get("payment_url")
    except Exception as e:
        print(f"获取支付链接失败: {e}")
        return None

@app.route('/upload', methods=['POST'])
def upload_file():
    user_id = session.get('user_id', str(uuid.uuid4()))
    session['user_id'] = user_id
    
    if not TEST_MODE and not session.get('payment_verified'):
        charge_result = charge_user(user_id)
        if not charge_result.get('ok'):
            payment_url = charge_result.get('payment_url')
            if payment_url:
                return render_template('payment_required.html', payment_url=payment_url, test_mode=TEST_MODE)
            return '余额不足，请先充值', 402
        session['payment_verified'] = True
    
    if 'file' not in request.files:
        return '没有选择文件', 400
    file = request.files['file']
    if file.filename == '':
        return '没有选择文件', 400
    if file and allowed_file(file.filename):
        filename = str(uuid.uuid4()) + '.csv'
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        session['data_file'] = filename
        return redirect(url_for('analysis', filename=filename))
    return '不允许的文件格式', 400

@app.route('/analysis/<filename>')
def analysis(filename):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    df = pd.read_csv(filepath)
    df['订单日期'] = pd.to_datetime(df['订单日期'])
    
    daily_sales = df.groupby(df['订单日期'].dt.date)['销售金额'].sum()
    product_rank = df.groupby('产品名称').agg({'销售数量': 'sum', '销售金额': 'sum'}).sort_values('销售数量', ascending=False)
    channel_sales = df.groupby('销售渠道')['销售金额'].sum()
    
    df['订单日期_日期'] = df['订单日期'].dt.date
    total_days = (df['订单日期_日期'].max() - df['订单日期_日期'].min()).days + 1
    inventory_data = df.groupby('产品名称').agg({'销售数量': 'sum', '库存数量': 'last'}).reset_index()
    inventory_data['日均销量'] = inventory_data['销售数量'] / total_days
    inventory_data['预计断货天数'] = inventory_data.apply(
        lambda x: int(x['库存数量'] / x['日均销量']) if x['日均销量'] > 0 else 0, axis=1
    )
    inventory_data['预计断货日期'] = inventory_data.apply(
        lambda x: (datetime.now() + timedelta(days=x['预计断货天数'])).strftime('%Y-%m-%d'), axis=1
    )
    
    charts = {}
    
    plt.figure(figsize=(10, 6))
    daily_sales.plot(kind='line', marker='o', color='blue')
    plt.title('日销售趋势图')
    plt.xlabel('日期')
    plt.ylabel('销售金额')
    plt.xticks(rotation=45)
    plt.tight_layout()
    daily_chart_filename = f'daily_sales_{filename}.png'
    daily_chart_path = os.path.join(SKILL_ROOT, 'static', 'charts', daily_chart_filename)
    plt.savefig(daily_chart_path)
    plt.close()
    charts['daily'] = url_for('static', filename=f'charts/{daily_chart_filename}')
    
    plt.figure(figsize=(10, 6))
    product_rank['销售数量'].plot(kind='bar', color='green')
    plt.title('产品销售数量排名')
    plt.xlabel('产品名称')
    plt.ylabel('销售数量')
    plt.xticks(rotation=45)
    plt.tight_layout()
    product_chart_filename = f'product_rank_{filename}.png'
    product_chart_path = os.path.join(SKILL_ROOT, 'static', 'charts', product_chart_filename)
    plt.savefig(product_chart_path)
    plt.close()
    charts['product'] = url_for('static', filename=f'charts/{product_chart_filename}')
    
    plt.figure(figsize=(10, 6))
    channel_sales.plot(kind='pie', autopct='%1.1f%%', colors=['red', 'blue', 'green', 'orange'])
    plt.title('各渠道收入占比')
    channel_chart_filename = f'channel_sales_{filename}.png'
    channel_chart_path = os.path.join(SKILL_ROOT, 'static', 'charts', channel_chart_filename)
    plt.savefig(channel_chart_path)
    plt.close()
    charts['channel'] = url_for('static', filename=f'charts/{channel_chart_filename}')
    
    session['charts'] = charts
    session['inventory_data'] = inventory_data.to_dict('records')
    
    return render_template('analysis.html',
                           daily_sales=daily_sales.to_dict(),
                           product_rank=product_rank.to_dict('index'),
                           channel_sales=channel_sales.to_dict(),
                           inventory_data=inventory_data.to_dict('records'),
                           charts=charts,
                           filename=filename)

@app.route('/generate_pdf/<filename>', methods=['POST'])
def generate_pdf(filename):
    cost_data = request.form.to_dict()
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    df = pd.read_csv(filepath)
    
    df['订单日期'] = pd.to_datetime(df['订单日期'])
    product_rank = df.groupby('产品名称').agg({'销售数量': 'sum', '销售金额': 'sum'}).sort_values('销售数量', ascending=False)
    
    pdf_filename = f'电商数据分析报告_{datetime.now().strftime("%Y%m%d%H%M%S")}.pdf'
    pdf_path = os.path.join(SKILL_ROOT, 'reports', pdf_filename)
    
    # 使用Canvas直接绘制，加载中文字体
    c = canvas.Canvas(pdf_path, pagesize=letter)
    width, height = letter
    
    # 标题（避免使用加粗的中文字体）
    if FONT_NAME == 'Helvetica':
        c.setFont("Helvetica-Bold", 24)
    else:
        c.setFont(FONT_NAME, 24)
    c.drawString(100, height - 100, "电商数据分析报告")
    
    # 生成时间
    c.setFont(FONT_NAME, 12)
    c.drawString(100, height - 130, f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 1. 产品销售排名
    if FONT_NAME == 'Helvetica':
        c.setFont("Helvetica-Bold", 16)
    else:
        c.setFont(FONT_NAME, 16)
    c.drawString(100, height - 180, "1. 产品销售排名")
    
    y = height - 210
    c.setFont(FONT_NAME, 10)
    # 表头
    c.drawString(100, y, "产品名称")
    c.drawString(300, y, "销售数量")
    c.drawString(450, y, "销售金额")
    y -= 20
    
    # 数据
    product_list = list(product_rank.iterrows())
    for i, (name, data) in enumerate(product_list):
        c.drawString(100, y, str(name))
        c.drawString(300, y, str(int(data['销售数量'])))
        c.drawString(450, y, f"${data['销售金额']:.2f}")
        y -= 20
        if y < 100:
            c.showPage()
            y = height - 50
    
    # 2. 利润率分析
    if y < 200:
        c.showPage()
        y = height - 50
    
    if FONT_NAME == 'Helvetica':
        c.setFont("Helvetica-Bold", 16)
    else:
        c.setFont(FONT_NAME, 16)
    c.drawString(100, y, "2. 利润率分析")
    y -= 30
    
    c.setFont(FONT_NAME, 10)
    # 表头
    c.drawString(80, y, "产品")
    c.drawString(200, y, "单位成本")
    c.drawString(320, y, "数量")
    c.drawString(420, y, "总收入")
    c.drawString(520, y, "总成本")
    c.drawString(600, y, "利润")
    c.drawString(700, y, "利润率(%)")
    y -= 20
    
    # 数据
    profit_list = list(product_rank.iterrows())
    for i, (name, data) in enumerate(profit_list):
        cost_key = f"{name}_cost"
        unit_cost = float(cost_data.get(cost_key, 0)) if cost_data.get(cost_key) else 0
        total_revenue = data['销售金额']
        total_cost = unit_cost * data['销售数量']
        profit = total_revenue - total_cost
        profit_rate = (profit / total_revenue * 100) if total_revenue > 0 else 0
        
        c.drawString(80, y, str(name))
        c.drawString(200, y, f"${unit_cost:.2f}")
        c.drawString(320, y, str(int(data['销售数量'])))
        c.drawString(420, y, f"${total_revenue:.2f}")
        c.drawString(520, y, f"${total_cost:.2f}")
        c.drawString(600, y, f"${profit:.2f}")
        c.drawString(700, y, f"{profit_rate:.1f}%")
        y -= 20
        if y < 100:
            c.showPage()
            y = height - 50
    
    # 3. 库存预警
    inventory_data = session.get('inventory_data', [])
    if inventory_data:
        if y < 200:
            c.showPage()
            y = height - 50
        
        if FONT_NAME == 'Helvetica':
            c.setFont("Helvetica-Bold", 16)
        else:
            c.setFont(FONT_NAME, 16)
        c.drawString(100, y, "3. 库存预警")
        y -= 30
        
        c.setFont(FONT_NAME, 10)
        # 表头
        c.drawString(100, y, "产品")
        c.drawString(280, y, "当前库存")
        c.drawString(380, y, "日均销量")
        c.drawString(500, y, "预计断货天数")
        c.drawString(630, y, "预计断货日期")
        y -= 20
        
        # 数据
        for i, item in enumerate(inventory_data):
            c.drawString(100, y, str(item['产品名称']))
            c.drawString(280, y, str(int(item['库存数量'])))
            c.drawString(380, y, f"{item['日均销量']:.1f}")
            c.drawString(500, y, str(int(item['预计断货天数'])))
            c.drawString(630, y, str(item['预计断货日期']))
            y -= 20
            if y < 100:
                c.showPage()
                y = height - 50
    
    c.save()
    return send_file(pdf_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
