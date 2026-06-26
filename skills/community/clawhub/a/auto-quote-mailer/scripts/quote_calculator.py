"""
Quotation Calculator
Calculate quotation based on material, size, process and quantity
报价计算器
根据材质、尺寸、工艺、数量计算报价
"""

import re

# ==============================================
# Replace the following pricing data with your own
# 请将以下报价数据替换为您自己的
# ==============================================

# Material base prices / 材质基础价格
# Example for custom medal business / 奖牌定制行业示例
MATERIAL_PRICES = [
    {
        'material': '金箔/实木类',
        'description': 'Classic style for authorization plaques',
        'retail_price': 85,
        'bulk_price': 45,
    },
    {
        'material': '水晶/琉璃类',
        'description': 'Transparent shiny for anniversaries',
        'retail_price': 120,
        'bulk_price': 65,
    },
    {
        'material': '金属开模类',
        'description': 'Heavy texture with relief for high-end events',
        'retail_price': 180,
        'bulk_price': 90,
        'mold_fee': True,
    },
    {
        'material': '亚克力/复合类',
        'description': 'Colorful various shapes for creative activities',
        'retail_price': 55,
        'bulk_price': 28,
    }
]

# Size coefficients / 尺寸系数
SIZE_COEFFICIENTS = {
    'S': {'range': 'under 15cm', 'coefficient': 0.8},
    'M': {'range': '15cm - 25cm', 'coefficient': 1.0},
    'L': {'range': '25cm - 40cm', 'coefficient': 1.5},
    'XL': {'range': 'over 40cm', 'coefficient': None},  # Need manual quote
}

# Additional process fees / 工艺附加费
PROCESS_FEES = {
    'laser_3d': {'name': '3D Laser Engraving', 'fee': 20, 'note': 'For crystal only'},
    'uv_print': {'name': 'UV Color Printing', 'fee': 10, 'note': 'Good for complex logos'},
    'etching': {'name': 'Metal Etching + Paint', 'fee': 30, 'note': 'Durable, never fade'},
    'gold_foil': {'name': 'Gold Foil Stamping', 'fee': 5, 'note': 'For text on wood'},
    'wood_box': {'name': 'Premium Wooden Box', 'fee': 35, 'note': 'Gift packaging'},
    'heavy_base': {'name': 'Heavy Marble Base', 'fee': 25, 'note': 'More premium feel'},
}

# Quantity tiers discount / 阶梯折扣
DISCOUNTS = [
    {'min': 1, 'max': 5, 'discount': 1.00, 'name': 'Retail'},
    {'min': 6, 'max': 20, 'discount': 0.95, 'name': 'Small bulk'},
    {'min': 21, 'max': 100, 'discount': 0.85, 'name': 'Medium bulk'},
    {'min': 101, 'max': None, 'discount': 0.70, 'name': 'Large bulk'},
]

# ==============================================
# End of pricing data - modify above for your business
# 报价数据结束 - 以上内容请根据您的业务修改
# ==============================================

def get_discount(quantity):
    """Get discount based on quantity"""
    for d in DISCOUNTS:
        if d['max'] is None:
            if quantity >= d['min']:
                return d
        elif d['min'] <= quantity <= d['max']:
            return d
    return DISCOUNTS[0]

def get_size_coefficient(size_cm):
    """Get coefficient based on size"""
    if size_cm < 15:
        return SIZE_COEFFICIENTS['S']
    elif 15 <= size_cm <= 25:
        return SIZE_COEFFICIENTS['M']
    elif 25 < size_cm <= 40:
        return SIZE_COEFFICIENTS['L']
    else:
        return SIZE_COEFFICIENTS['XL']

def get_material_base_price(material_name, quantity):
    """Get base price based on material and quantity"""
    for mat in MATERIAL_PRICES:
        if mat['material'] == material_name or material_name in mat['material']:
            if quantity >= 50:
                return mat['bulk_price'], mat
            else:
                return mat['retail_price'], mat
    return None, None

def calculate_price(material, size_cm, quantity, processes=None):
    """
    Calculate total price
    
    Parameters:
        material: material name
        size_cm: size in centimeters
        quantity: quantity
        processes: list of process keys, e.g. ['uv_print', 'wood_box']
    
    Returns:
        dict: detailed price calculation result
    """
    processes = processes or []
    
    # Get base price
    base_price, material_info = get_material_base_price(material, quantity)
    if base_price is None:
        return {'error': 'Unknown material'}
    
    # Get size coefficient
    size_info = get_size_coefficient(size_cm)
    if size_info['coefficient'] is None:
        return {'error': 'Size too large, requires manual quotation'}
    
    # Calculate base price
    price_per_unit = base_price * size_info['coefficient']
    
    # Add process fees
    process_fee_total = 0
    process_list = []
    for p in processes:
        if p in PROCESS_FEES:
            fee = PROCESS_FEES[p]['fee']
            process_fee_total += fee
            process_list.append({
                'name': PROCESS_FEES[p]['name'],
                'fee': fee
            })
    price_per_unit += process_fee_total
    
    # Get discount
    discount_info = get_discount(quantity)
    total_price = price_per_unit * quantity * discount_info['discount']
    
    return {
        'base_price': base_price,
        'size_cm': size_cm,
        'size_coefficient': size_info['coefficient'],
        'quantity': quantity,
        'process_fees': process_list,
        'process_fee_total': process_fee_total,
        'price_per_unit': price_per_unit,
        'discount_rate': discount_info['discount'],
        'discount_name': discount_info['name'],
        'total_price': total_price,
        'material': material,
        'material_description': material_info['description'] if material_info else '',
    }

def parse_customer_request(text):
    """
    Parse customer requirements from inquiry text
    Attempt to extract: material, size, quantity, process requirements
    从客户询价文本解析需求，尝试提取: 材质、尺寸、数量、工艺要求
    """
    # Simple keyword extraction / 简单关键词提取
    material = None
    
    # Detect material keywords - add your own keywords here
    # 检测材质关键词 - 请在这里添加您自己的关键词
    material_keywords = {
        '水晶': '水晶/琉璃类',
        '玻璃': '水晶/琉璃类',
        '琉璃': '水晶/琉璃类',
        '金箔': '金箔/实木类',
        '实木': '金箔/实木类',
        '木头': '金箔/实木类',
        '木质': '金箔/实木类',
        '金属': '金属开模类',
        '合金': '金属开模类',
        '铜': '金属开模类',
        '不锈钢': '金属开模类',
        '亚克力': '亚克力/复合类',
        '复合': '亚克力/复合类',
    }
    for kw, mat in material_keywords.items():
        if kw in text:
            material = mat
            break
    
    # Extract quantity / 尝试提取数量
    quantity = 1
    numbers = re.findall(r'(\d+)(个|件|只|pcs|piece|pc)', text.lower())
    if numbers:
        quantity = int(numbers[0][0])
    
    # Extract size / 尝试提取尺寸
    size = None
    size_matches = re.findall(r'(\d+)\s*cm|(\d+)\s*厘米|(\d+)\s*公分', text.lower())
    if size_matches:
        for match in size_matches:
            num = next((m for m in match if m), None)
            if num:
                size = int(num)
                break
    
    # Detect processes / 检测工艺
    processes = []
    # Add your own process keywords here
    # 请在这里添加您自己的工艺关键词
    process_keywords = {
        'uv': 'uv_print',
        '喷印': 'uv_print',
        '印刷': 'uv_print',
        '激光': 'laser_3d',
        '内雕': 'laser_3d',
        '雕刻': 'etching',
        '蚀刻': 'etching',
        '填漆': 'etching',
        '金箔': 'gold_foil',
        '烫印': 'gold_foil',
        '木盒': 'wood_box',
        '礼盒': 'wood_box',
        '包装盒': 'wood_box',
        '底座': 'heavy_base',
        '加重': 'heavy_base',
    }
    for kw, proc in process_keywords.items():
        if kw in text:
            processes.append(proc)
    
    return {
        'material': material,
        'quantity': quantity,
        'size': size,
        'processes': processes,
        'original_text': text,
    }

def generate_quote_text(quote_result, company_info):
    """Generate Chinese quotation reply text / 生成中文报价回复文本"""
    if 'error' in quote_result:
        return f"""错误: {quote_result['error']}

请提供更详细信息给客户进行人工报价。
"""
    
    template = f"""尊敬的客户：

感谢您的询价，以下是我们为您提供的报价：

产品信息：
- 材质：{quote_result['material']}
- 尺寸：{quote_result['size_cm']} cm
- 数量：{quote_result['quantity']} 个
- 折扣：{quote_result['discount_name']} ({int(quote_result['discount_rate'] * 100)}折)

价格明细：
- 基础单价：¥{quote_result['base_price']:.2f}
- 尺寸系数：{quote_result['size_coefficient']}
"""
    
    if quote_result['process_fees']:
        template += "\n附加工艺：\n"
        for p in quote_result['process_fees']:
            template += f"- {p['name']}: +¥{p['fee']}\n"
    
    template += f"""
计算结果：
- 单价：¥{quote_result['price_per_unit']:.2f} /个
- 总计：**¥{quote_result['total_price']:.2f}**

备注说明：
- 价格已包含标准包装
- 确认设计稿后，普通材质24小时内出样
- 运输途中破损，拍照核实后100%免费重做
- 单笔订单满¥2000包邮（国内）

联系人：{company_info['contact_person']}
联系电话：{company_info['phone']}
企业官网：{company_info['website']}
邮箱：{company_info['email']}

期待为您服务！

{company_info['name']}
"""
    return template


def generate_quote_text_in_language(quote_result, company_info, lang='en'):
    """Generate quotation reply in other languages / 生成其他语言报价回复"""
    if 'error' in quote_result:
        return f"""Error: {quote_result['error']}

Please provide more information for manual quotation.
"""
    
    discount_percent = int(quote_result['discount_rate'] * 100)
    
    template = f"""Dear Customer,

Thank you for your inquiry. Here is our quotation:

Product Information:
- Material: {quote_result['material']}
- Size: {quote_result['size_cm']} cm
- Quantity: {quote_result['quantity']} pieces
- Discount: {quote_result['discount_name']} ({discount_percent}%)

Price Breakdown:
- Base unit price: ¥{quote_result['base_price']:.2f}
- Size coefficient: {quote_result['size_coefficient']}
"""
    
    if quote_result['process_fees']:
        template += "\nAdditional Processes:\n"
        for p in quote_result['process_fees']:
            template += f"- {p['name']}: +¥{p['fee']}\n"
    
    template += f"""
Calculation Result:
- Unit price: ¥{quote_result['price_per_unit']:.2f} /pc
- Total price: **¥{quote_result['total_price']:.2f}**

Notes:
- Standard packaging is included
- Sample ready within 24 hours after design confirmation
- If damaged during shipping, we will 100% re-make for free after photo confirmation
- Free shipping (domestic) for orders over ¥2000

Contact:
Contact person: {company_info['contact_person']}
Phone: {company_info['phone']}
Website: {company_info['website']}
Email: {company_info['email']}

We look forward to serving you!

Best regards,
{company_info['name']}
"""
    return template
