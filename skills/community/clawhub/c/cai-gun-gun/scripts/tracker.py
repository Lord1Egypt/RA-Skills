#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
记账财滚滚 v2.0 - 核心记账脚本
支持：添加、删除、查询、统计、导出、报告生成、导入
数据结构：与第三方格式兼容
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, List, Dict, Any

# 数据目录配置（双存储：主数据+同步备份）
import os
import shutil
SKILL_DIR = Path(__file__).parent.parent

# 主数据目录（跨平台，用于本地存储）
# 默认：~/.cai-gun-gun/data/
# 可通过环境变量 CAI_GUN_GUN_DATA_DIR 自定义
PRIMARY_DATA_DIR = Path(os.environ.get(
    "CAI_GUN_GUN_DATA_DIR", 
    str(Path.home() / ".cai-gun-gun" / "data")
))

# 同步数据目录（在skill目录下，用于云同步）
# 如果agent有skill云同步能力，这个目录会被同步
SYNC_DATA_DIR = SKILL_DIR / "data"

# 确保目录存在
PRIMARY_DATA_DIR.mkdir(parents=True, exist_ok=True)
SYNC_DATA_DIR.mkdir(parents=True, exist_ok=True)

# 为了向后兼容，DATA_DIR指向主数据目录
DATA_DIR = PRIMARY_DATA_DIR

# 数据文件列表
DATA_FILES = ["transactions.json", "accounts.json", "categories.json", "config.json"]


def sync_to_skill():
    """将主数据目录同步到skill目录（用于云同步）"""
    try:
        for filename in DATA_FILES:
            src = PRIMARY_DATA_DIR / filename
            dst = SYNC_DATA_DIR / filename
            if src.exists():
                shutil.copy2(src, dst)
        return True
    except Exception as e:
        print(f"同步到skill目录失败: {e}", file=sys.stderr)
        return False


def sync_from_skill():
    """从skill目录同步到主数据目录（恢复数据）"""
    try:
        for filename in DATA_FILES:
            src = SYNC_DATA_DIR / filename
            dst = PRIMARY_DATA_DIR / filename
            if src.exists():
                shutil.copy2(src, dst)
        return True
    except Exception as e:
        print(f"从skill目录同步失败: {e}", file=sys.stderr)
        return False

TRANSACTIONS_FILE = DATA_DIR / "transactions.json"
ACCOUNTS_FILE = DATA_DIR / "accounts.json"
CATEGORIES_FILE = DATA_DIR / "categories.json"
CONFIG_FILE = DATA_DIR / "config.json"

# ==================== 第三方兼容的分类体系 ====================
# 一级分类: 二级分类列表
DEFAULT_CATEGORIES = {
    "expense": {
        "食品水果": ["餐饮", "买菜", "零食", "水果", "茶饮", "咖啡"],
        "出行交通": ["交通", "打车", "用车", "火车票", "租车"],
        "购物消费": ["购物", "电子产品", "衣服鞋包", "淘宝", "京东"],
        "生活服务": ["生活用品", "彩妆洗漱", "家电", "家具", "理发", "洗衣", "快递", "打印"],
        "住房成本": ["房租", "水电", "物业", "宽带", "维修"],
        "娱乐休闲": ["电影", "游戏", "KTV", "旅游", "运动", "会员"],
        "医疗健康": ["药品", "看病", "体检"],
        "教育培训": ["书籍", "文具", "学费", "课程", "培训"],
        "社交人情": ["红包", "礼物", "请客", "人情"],
        "通讯网络": ["话费", "上网"],
        "茶水饮料": ["酒水饮料", "奶茶", "咖啡", "茶叶"],
        "网络资源": ["服务器", "软件", "会员订阅"],
        "保险保障": ["保险"],
        "其他支出": ["其他", "捐赠", "宠物", "彩票"]
    },
    "income": {
        "工资收入": ["基本工资", "奖金", "绩效", "加班费"],
        "投资收益": ["股票", "基金", "理财", "分红"],
        "副业收入": ["兼职", "稿费", "接单", "副业"],
        "其他收入": ["红包", "退款", "报销", "其他"]
    }
}

# 默认账户
DEFAULT_ACCOUNTS = [
    {"id": "cash", "name": "现金", "emoji": "💵", "balance": 0},
    {"id": "wechat", "name": "微信钱包", "emoji": "💳", "balance": 0},
    {"id": "alipay", "name": "支付宝余额", "emoji": "💰", "balance": 0},
    {"id": "bankcard", "name": "银行卡", "emoji": "🏦", "balance": 0},
    {"id": "creditcard", "name": "信用卡", "emoji": "💳", "balance": 0}
]

# 分类关键词映射（用于智能推断）
# 格式: 二级分类 -> 关键词列表
CATEGORY_KEYWORDS = {
    # 食品水果
    "餐饮": ["吃饭", "午餐", "晚餐", "早餐", "午饭", "晚饭", "早饭", "外卖", "饭店", "餐厅", "食堂", "点餐", "套餐", "饭", "面", "饺子"],
    "买菜": ["买菜", "超市", "菜市场", "蔬菜", "肉类", "生鲜"],
    "零食": ["零食", "小吃", "薯片", "饼干", "瓜子"],
    "水果": ["水果", "苹果", "香蕉", "西瓜", "葡萄", "橙子"],
    "茶饮": ["茶", "茶叶", "奶茶", "饮品", "饮料"],
    "咖啡": ["咖啡", "星巴克", "瑞幸", "拿铁", "美式"],
    
    # 出行交通
    "交通": ["地铁", "公交", "巴士", "出行", "交通", "地铁公交"],
    "打车": ["打车", "滴滴", "出租车", "网约车", "的士"],
    "用车": ["加油", "停车", "洗车", "保养", "油费"],
    "火车票": ["火车", "高铁", "动车", "火车票"],
    "租车": ["租车", "共享汽车"],
    
    # 购物消费
    "购物": ["购物", "买", "淘宝", "京东", "拼多多"],
    "电子产品": ["手机", "电脑", "耳机", "数码", "电器", "电子产品"],
    "衣服鞋包": ["衣服", "鞋", "包", "裤子", "外套", "T恤", "衣服鞋包"],
    
    # 生活服务
    "生活用品": ["日用品", "超市", "洗护", "纸巾", "生活用品"],
    "理发": ["理发", "美发", "剪发", "烫发"],
    "快递": ["快递", "邮寄", "发货"],
    
    # 住房成本
    "房租": ["房租", "租金", "住房"],
    "水电": ["水费", "电费", "水电"],
    "宽带": ["宽带", "网费", "网络"],
    
    # 娱乐休闲
    "电影": ["电影", "影院", "观影"],
    "游戏": ["游戏", "steam", "手游", "充值", "游戏充值"],
    "旅游": ["旅游", "景点", "门票", "酒店"],
    "会员": ["会员", "订阅", "VIP", "年费", "会员订阅"],
    
    # 医疗健康
    "药品": ["药", "药店", "药品", "买药"],
    "看病": ["医院", "看病", "挂号", "门诊"],
    "体检": ["体检", "检查"],
    
    # 教育培训
    "书籍": ["书", "书籍", "电子书"],
    "课程": ["课程", "网课", "培训", "学习"],
    
    # 社交人情
    "红包": ["红包", "转账"],
    "礼物": ["礼物", "礼品", "送礼"],
    "请客": ["请客", "聚餐", "宴请"],
    
    # 通讯网络
    "话费": ["话费", "充值", "手机费"],
    "上网": ["流量", "上网", "WiFi"],
    
    # 收入
    "基本工资": ["工资", "薪水", "月薪", "基本工资"],
    "奖金": ["奖金", "年终奖", "绩效奖"],
    "兼职": ["兼职", "副业", "外快"],
    "报销": ["报销", "退款", "返还"],
}


# ==================== 数据操作函数 ====================

def ensure_data_dir():
    """确保数据目录存在（已弃用，现在使用 PRIMARY_DATA_DIR 和 SYNC_DATA_DIR）"""
    PRIMARY_DATA_DIR.mkdir(parents=True, exist_ok=True)
    SYNC_DATA_DIR.mkdir(parents=True, exist_ok=True)


def load_transactions() -> List[Dict]:
    """加载交易记录（容错处理，支持双存储）"""
    PRIMARY_DATA_DIR.mkdir(parents=True, exist_ok=True)
    SYNC_DATA_DIR.mkdir(parents=True, exist_ok=True)
    
    # 先尝试主数据目录
    if TRANSACTIONS_FILE.exists():
        try:
            with open(TRANSACTIONS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            pass  # 主文件损坏，尝试从同步目录恢复
    
    # 主文件不存在或损坏，尝试同步目录
    sync_file = SYNC_DATA_DIR / "transactions.json"
    if sync_file.exists():
        try:
            with open(sync_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # 恢复到主目录
                with open(TRANSACTIONS_FILE, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                sync_to_skill()  # 确保同步
                print(f"从同步目录恢复交易记录", file=sys.stderr)
                return data
        except json.JSONDecodeError:
            pass
    
    return []


def save_transactions(transactions: List[Dict]):
    """保存交易记录（双存储）"""
    PRIMARY_DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(TRANSACTIONS_FILE, 'w', encoding='utf-8') as f:
        json.dump(transactions, f, ensure_ascii=False, indent=2)
    sync_to_skill()  # 同步到skill目录


def load_accounts() -> Dict:
    """加载账户（支持双存储）"""
    PRIMARY_DATA_DIR.mkdir(parents=True, exist_ok=True)
    SYNC_DATA_DIR.mkdir(parents=True, exist_ok=True)
    
    # 先尝试主数据目录
    if ACCOUNTS_FILE.exists():
        try:
            with open(ACCOUNTS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            pass
    
    # 尝试同步目录
    sync_file = SYNC_DATA_DIR / "accounts.json"
    if sync_file.exists():
        try:
            with open(sync_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                with open(ACCOUNTS_FILE, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                sync_to_skill()
                return data
        except (json.JSONDecodeError, IOError):
            pass
    
    # 初始化默认账户
    accounts = {acc["id"]: acc for acc in DEFAULT_ACCOUNTS}
    save_accounts(accounts)
    return accounts


def save_accounts(accounts: Dict):
    """保存账户（双存储）"""
    PRIMARY_DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(ACCOUNTS_FILE, 'w', encoding='utf-8') as f:
        json.dump(accounts, f, ensure_ascii=False, indent=2)
    sync_to_skill()


def load_categories() -> Dict:
    """加载分类（支持双存储）"""
    PRIMARY_DATA_DIR.mkdir(parents=True, exist_ok=True)
    SYNC_DATA_DIR.mkdir(parents=True, exist_ok=True)
    
    # 先尝试主数据目录
    if CATEGORIES_FILE.exists():
        try:
            with open(CATEGORIES_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            pass
    
    # 尝试同步目录
    sync_file = SYNC_DATA_DIR / "categories.json"
    if sync_file.exists():
        try:
            with open(sync_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                with open(CATEGORIES_FILE, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                sync_to_skill()
                return data
        except (json.JSONDecodeError, IOError):
            pass
    
    save_categories(DEFAULT_CATEGORIES)
    return DEFAULT_CATEGORIES


def save_categories(categories: Dict):
    """保存分类（双存储）"""
    PRIMARY_DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(CATEGORIES_FILE, 'w', encoding='utf-8') as f:
        json.dump(categories, f, ensure_ascii=False, indent=2)
    sync_to_skill()


def load_config() -> Dict:
    """加载配置"""
    ensure_data_dir()
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"default_account": "wechat"}


def save_config(config: Dict):
    """保存配置（双存储）"""
    PRIMARY_DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)
    sync_to_skill()


# ==================== 核心功能函数 ====================

def infer_category(note: str, tx_type: str = "expense") -> tuple:
    """根据备注推断分类"""
    note_lower = note.lower()
    
    # 查找最佳匹配
    best_match = None
    best_score = 0
    
    for subcat, keywords in CATEGORY_KEYWORDS.items():
        for keyword in keywords:
            if keyword in note_lower:
                score = len(keyword)
                if score > best_score:
                    best_score = score
                    best_match = subcat
    
    if best_match:
        # 找到一级分类
        categories = load_categories()
        type_cats = categories.get(tx_type, {})
        for main_cat, subcats in type_cats.items():
            if best_match in subcats:
                return main_cat, best_match
    
    # 默认分类
    if tx_type == "expense":
        return "其他支出", "其他"
    return "其他收入", "其他"


def get_account_by_name(name: str) -> Optional[Dict]:
    """根据名称获取账户"""
    accounts = load_accounts()
    for acc_id, acc in accounts.items():
        if acc["name"] == name:
            return acc
    return None


def update_account_balance(account_name: str, amount: float, tx_type: str):
    """更新账户余额"""
    accounts = load_accounts()
    
    for acc_id, acc in accounts.items():
        if acc["name"] == account_name:
            current = acc.get("balance", 0)
            if tx_type == "income":
                new_balance = current + amount
            else:
                new_balance = current - amount
            accounts[acc_id]["balance"] = round(new_balance, 2)
            save_accounts(accounts)
            return True
    return False


def add_transaction(
    tx_type: str,
    amount: float,
    category: Optional[str] = None,
    subcategory: Optional[str] = None,
    account: Optional[str] = None,
    note: Optional[str] = None,
    date: Optional[str] = None,
    time: Optional[str] = None,
    member: Optional[str] = None,
    merchant: Optional[str] = None
) -> Dict:
    """添加交易记录（第三方格式）"""
    ensure_data_dir()
    transactions = load_transactions()
    
    # 验证交易类型
    if tx_type not in ["expense", "income"]:
        tx_type = "expense"
    
    # 推断分类
    if not category:
        category, subcategory = infer_category(note or "", tx_type)
    else:
        # 确保分类存在
        ensure_category_exists(tx_type, category, subcategory)
    
    # 默认账户
    if not account:
        config = load_config()
        default_acc_id = config.get("default_account", "wechat")
        accounts = load_accounts()
        account = accounts.get(default_acc_id, {}).get("name", "微信钱包")
    
    # 日期时间
    now = datetime.now()
    if not date:
        date = now.strftime("%Y-%m-%d")
    if not time:
        time = now.strftime("%H:%M:%S")
    
    # 构建交易记录（第三方格式）
    transaction = {
        "id": f"tx_{now.strftime('%Y%m%d%H%M%S')}_{len(transactions)}",
        "交易类型": "支出" if tx_type == "expense" else "收入",
        "日期": f"{date} {time}",
        "一级分类": category,
        "二级分类": subcategory or "",
        "账户1": account,
        "账户2": None,
        "账户币种": "CNY",
        "金额": round(amount, 2),
        "成员": member or "",
        "商家": merchant or "",
        "项目分类": None,
        "项目": None,
        "记账人": "QClaw",
        "备注": note or "",
        # 额外字段（内部使用）
        "_internal": {
            "type": tx_type,
            "created_at": now.isoformat()
        }
    }
    
    transactions.append(transaction)
    save_transactions(transactions)
    
    # 更新账户余额
    update_account_balance(account, amount, tx_type)
    
    return transaction


def ensure_category_exists(tx_type: str, category: str, subcategory: Optional[str] = None):
    """确保分类存在，不存在则添加"""
    categories = load_categories()
    type_cats = categories.get(tx_type, {})
    
    if category not in type_cats:
        type_cats[category] = []
    
    if subcategory and subcategory not in type_cats[category]:
        type_cats[category].append(subcategory)
    
    categories[tx_type] = type_cats
    save_categories(categories)


def delete_transaction(tx_id: Optional[str] = None, note: Optional[str] = None) -> bool:
    """删除交易记录"""
    transactions = load_transactions()
    
    if not transactions:
        return False
    
    deleted_tx = None
    
    if tx_id:
        for t in transactions:
            if t.get("id") == tx_id:
                deleted_tx = t
                break
        transactions = [t for t in transactions if t.get("id") != tx_id]
    elif note:
        for t in reversed(transactions):
            if note in t.get("备注", ""):
                deleted_tx = t
                transactions.remove(t)
                break
    
    save_transactions(transactions)
    
    # 回滚余额
    if deleted_tx:
        internal = deleted_tx.get("_internal", {})
        tx_type = internal.get("type", "expense")
        amount = deleted_tx.get("金额", 0)
        account = deleted_tx.get("账户1", "")
        
        # 反向更新余额
        accounts = load_accounts()
        for acc_id, acc in accounts.items():
            if acc["name"] == account:
                current = acc.get("balance", 0)
                if tx_type == "income":
                    new_balance = current - amount
                else:
                    new_balance = current + amount
                accounts[acc_id]["balance"] = round(new_balance, 2)
                save_accounts(accounts)
                break
    
    return deleted_tx is not None


def list_transactions(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    tx_type: Optional[str] = None,
    category: Optional[str] = None,
    limit: Optional[int] = None
) -> List[Dict]:
    """查询交易记录"""
    transactions = load_transactions()
    
    # 过滤
    if start_date:
        transactions = [t for t in transactions if t.get("日期", "") >= start_date]
    if end_date:
        transactions = [t for t in transactions if t.get("日期", "") <= end_date + " 23:59:59"]
    if tx_type:
        type_str = "支出" if tx_type == "expense" else "收入"
        transactions = [t for t in transactions if t.get("交易类型") == type_str]
    if category:
        transactions = [t for t in transactions if category in t.get("一级分类", "") or category in t.get("二级分类", "")]
    
    # 排序（最新的在前）
    transactions = sorted(transactions, key=lambda x: x.get("日期", ""), reverse=True)
    
    if limit:
        transactions = transactions[:limit]
    
    return transactions


def get_summary(period: str = "month") -> Dict:
    """统计汇总"""
    transactions = load_transactions()
    
    now = datetime.now()
    if period == "month":
        start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        start_str = start.strftime("%Y-%m-%d")
    elif period == "week":
        start = now - timedelta(days=now.weekday())
        start = start.replace(hour=0, minute=0, second=0, microsecond=0)
        start_str = start.strftime("%Y-%m-%d")
    elif period == "year":
        start = now.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
        start_str = start.strftime("%Y-%m-%d")
    else:
        start_str = "1970-01-01"
    
    # 过滤时间段内的交易
    filtered = [t for t in transactions if t.get("日期", "") >= start_str]
    
    # 统计
    total_expense = sum(t.get("金额", 0) for t in filtered if t.get("交易类型") == "支出")
    total_income = sum(t.get("金额", 0) for t in filtered if t.get("交易类型") == "收入")
    
    # 按分类统计
    category_stats = {}
    for t in filtered:
        cat = t.get("一级分类", "其他")
        if cat not in category_stats:
            category_stats[cat] = {"amount": 0, "count": 0}
        category_stats[cat]["amount"] += t.get("金额", 0)
        category_stats[cat]["count"] += 1
    
    return {
        "period": period,
        "start_date": start_str,
        "total_expense": round(total_expense, 2),
        "total_income": round(total_income, 2),
        "balance": round(total_income - total_expense, 2),
        "transaction_count": len(filtered),
        "category_stats": category_stats
    }


def get_accounts_summary() -> List[Dict]:
    """获取账户余额汇总"""
    accounts = load_accounts()
    result = []
    for acc_id, acc in accounts.items():
        result.append({
            "id": acc_id,
            "name": acc["name"],
            "emoji": acc.get("emoji", ""),
            "balance": acc.get("balance", 0)
        })
    return result


def import_from_excel(file_path: str) -> Dict:
    """从Excel导入（支持多sheet）"""
    try:
        import pandas as pd
    except ImportError:
        return {"success": False, "error": "需要安装pandas: pip install pandas openpyxl"}
    
    try:
        # 读取所有sheet
        xl = pd.ExcelFile(file_path)
        sheet_names = xl.sheet_names
        
        imported = 0
        errors = []
        new_transactions = []
        
        # 生成导入批次ID（避免ID冲突）
        import_batch = datetime.now().strftime('%Y%m%d%H%M%S')
        
        # 遍历所有sheet
        for sheet_name in sheet_names:
            df = pd.read_excel(file_path, sheet_name=sheet_name, header=0)
            
            for idx, row in df.iterrows():
                try:
                    tx_type_str = str(row.get("交易类型", sheet_name))  # 如果交易类型为空，用sheet名称
                    tx_type = "income" if "收入" in tx_type_str else "expense"
                    
                    date_str = str(row.get("日期", ""))
                    
                    transaction = {
                        "id": f"tx_import_{import_batch}_{sheet_name}_{idx}",
                        "交易类型": tx_type_str,
                        "日期": date_str,
                        "一级分类": str(row.get("一级分类", "其他")),
                        "二级分类": str(row.get("二级分类", "")),
                        "账户1": str(row.get("账户1", "现金")),
                        "账户2": str(row.get("账户2")) if pd.notna(row.get("账户2")) else None,
                        "账户币种": str(row.get("账户币种", "CNY")),
                        "金额": float(row.get("金额", 0)),
                        "成员": str(row.get("成员", "")) if pd.notna(row.get("成员")) else "",
                        "商家": str(row.get("商家", "")) if pd.notna(row.get("商家")) else "",
                        "项目分类": str(row.get("项目分类")) if pd.notna(row.get("项目分类")) else None,
                        "项目": str(row.get("项目")) if pd.notna(row.get("项目")) else None,
                        "记账人": str(row.get("记账人", "导入")),
                        "备注": str(row.get("备注", "")) if pd.notna(row.get("备注")) else "",
                        "_internal": {
                            "type": tx_type,
                            "created_at": datetime.now().isoformat(),
                            "imported": True,
                            "batch": import_batch,
                            "sheet": sheet_name
                        }
                    }
                    
                    new_transactions.append(transaction)
                    imported += 1
                    
                except Exception as e:
                    errors.append(f"Sheet[{sheet_name}]行{idx}: {str(e)}")
        
        # 批量保存：一次性加载+保存
        transactions = load_transactions()
        transactions.extend(new_transactions)
        save_transactions(transactions)
        
        # 批量更新账户余额
        accounts = load_accounts()
        for tx in new_transactions:
            internal = tx.get("_internal", {})
            tx_type = internal.get("type", "expense")
            amount = tx.get("金额", 0)
            account_name = tx.get("账户1", "")
            
            # 找到对应账户并更新余额
            for acc_id, acc in accounts.items():
                if acc["name"] == account_name:
                    current = acc.get("balance", 0)
                    if tx_type == "income":
                        new_balance = current + amount
                    else:
                        new_balance = current - amount
                    accounts[acc_id]["balance"] = round(new_balance, 2)
                    break
        
        save_accounts(accounts)
        
        return {
            "success": True,
            "imported": imported,
            "errors": errors[:10],
            "message": f"成功从{len(sheet_names)}个sheet导入{imported}条记录，已更新账户余额"
        }
        
    except Exception as e:
        return {"success": False, "error": str(e)}


def export_to_excel(output_path: Optional[str] = None) -> str:
    """导出到Excel（第三方格式，多sheet，完全还原导入格式）"""
    try:
        import pandas as pd
    except ImportError:
        return "需要安装pandas: pip install pandas openpyxl"
    
    transactions = load_transactions()
    
    if not transactions:
        return "没有交易记录可导出"
    
    # 按照sheet分组（还原导入时的格式）
    sheets_data = {}
    for t in transactions:
        # 获取来源sheet，如果没有则默认为"支出"
        sheet_name = t.get("_internal", {}).get("sheet", "支出")
        if sheet_name not in sheets_data:
            sheets_data[sheet_name] = []
        
        sheets_data[sheet_name].append({
            "交易类型": t.get("交易类型", ""),
            "日期": t.get("日期", ""),
            "一级分类": t.get("一级分类", ""),
            "二级分类": t.get("二级分类", ""),
            "账户1": t.get("账户1", ""),
            "账户2": t.get("账户2"),
            "账户币种": t.get("账户币种", "CNY"),
            "金额": t.get("金额", 0),
            "成员": t.get("成员", ""),
            "商家": t.get("商家", ""),
            "项目分类": t.get("项目分类"),
            "项目": t.get("项目"),
            "记账人": t.get("记账人", ""),
            "备注": t.get("备注", "")
        })
    
    # 生成文件名
    if not output_path:
        now = datetime.now()
        output_path = str(DATA_DIR / f"账单导出_{now.strftime('%Y%m%d_%H%M%S')}.xlsx")
    
    # 写入多个sheet（完全还原导入格式）
    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        for sheet_name, data in sheets_data.items():
            df = pd.DataFrame(data)
            df.to_excel(writer, sheet_name=sheet_name, index=False)
    
    return output_path
# ==================== CLI 入口 ====================

def main():
    parser = argparse.ArgumentParser(description="记账财滚滚 v2.0")
    subparsers = parser.add_subparsers(dest="command", help="命令")
    
    # add 命令
    add_parser = subparsers.add_parser("add", help="添加交易")
    add_parser.add_argument("--type", choices=["expense", "income"], default="expense")
    add_parser.add_argument("--amount", type=float, required=True)
    add_parser.add_argument("--category", help="一级分类")
    add_parser.add_argument("--subcategory", help="二级分类")
    add_parser.add_argument("--account", help="账户")
    add_parser.add_argument("--note", help="备注")
    add_parser.add_argument("--date", help="日期 YYYY-MM-DD")
    add_parser.add_argument("--time", help="时间 HH:MM:SS")
    add_parser.add_argument("--member", help="成员")
    add_parser.add_argument("--merchant", help="商家")
    
    # delete 命令
    delete_parser = subparsers.add_parser("delete", help="删除交易")
    delete_parser.add_argument("--id", help="交易ID")
    delete_parser.add_argument("--note", help="按备注匹配删除")
    
    # list 命令
    list_parser = subparsers.add_parser("list", help="查询交易")
    list_parser.add_argument("--start", help="开始日期")
    list_parser.add_argument("--end", help="结束日期")
    list_parser.add_argument("--type", choices=["expense", "income"])
    list_parser.add_argument("--category", help="分类")
    list_parser.add_argument("--limit", type=int, default=50)
    
    # summary 命令
    summary_parser = subparsers.add_parser("summary", help="统计汇总")
    summary_parser.add_argument("--period", choices=["week", "month", "year", "all"], default="month")
    
    # account 命令
    account_parser = subparsers.add_parser("account", help="账户管理")
    account_parser.add_argument("action", choices=["list", "add", "balance"])
    account_parser.add_argument("--name", help="账户名称")
    account_parser.add_argument("--balance", type=float, help="余额")
    account_parser.add_argument("--id", help="账户ID")
    
    # category 命令
    category_parser = subparsers.add_parser("category", help="分类管理")
    category_parser.add_argument("action", choices=["list", "add"])
    category_parser.add_argument("--type", choices=["expense", "income"], default="expense")
    category_parser.add_argument("--main", help="一级分类")
    category_parser.add_argument("--sub", help="二级分类")
    
    # export 命令
    export_parser = subparsers.add_parser("export", help="导出Excel")
    export_parser.add_argument("--output", "-o", help="输出路径")
    
    # import 命令
    import_parser = subparsers.add_parser("import", help="导入Excel")
    import_parser.add_argument("file", help="Excel文件路径")
    
    # clear 命令
    clear_parser = subparsers.add_parser("clear", help="清空数据")
    clear_parser.add_argument("--confirm", action="store_true", help="确认清空")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # 执行命令
    if args.command == "add":
        result = add_transaction(
            tx_type=args.type,
            amount=args.amount,
            category=args.category,
            subcategory=args.subcategory,
            account=args.account,
            note=args.note,
            date=args.date,
            time=args.time,
            member=args.member,
            merchant=args.merchant
        )
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    elif args.command == "delete":
        success = delete_transaction(tx_id=args.id, note=args.note)
        print(json.dumps({"success": success}, ensure_ascii=False))
    
    elif args.command == "list":
        result = list_transactions(
            start_date=args.start,
            end_date=args.end,
            tx_type=args.type,
            category=args.category,
            limit=args.limit
        )
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    elif args.command == "summary":
        result = get_summary(args.period)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    elif args.command == "account":
        if args.action == "list":
            result = get_accounts_summary()
            print(json.dumps(result, ensure_ascii=False, indent=2))
        elif args.action == "add":
            accounts = load_accounts()
            new_id = f"acc_{len(accounts)}"
            accounts[new_id] = {
                "id": new_id,
                "name": args.name,
                "emoji": "💳",
                "balance": args.balance or 0
            }
            save_accounts(accounts)
            print(json.dumps({"success": True, "id": new_id}, ensure_ascii=False))
        elif args.action == "balance":
            result = get_accounts_summary()
            print(json.dumps(result, ensure_ascii=False, indent=2))
    
    elif args.command == "category":
        if args.action == "list":
            categories = load_categories()
            print(json.dumps(categories, ensure_ascii=False, indent=2))
        elif args.action == "add":
            ensure_category_exists(args.type, args.main, args.sub)
            print(json.dumps({"success": True}, ensure_ascii=False))
    
    elif args.command == "export":
        result = export_to_excel(args.output)
        print(json.dumps({"path": result}, ensure_ascii=False))
    
    elif args.command == "import":
        result = import_from_excel(args.file)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    elif args.command == "clear":
        if args.confirm:
            save_transactions([])
            accounts = load_accounts()
            for acc_id in accounts:
                accounts[acc_id]["balance"] = 0
            save_accounts(accounts)
            print(json.dumps({"success": True, "message": "数据已清空"}, ensure_ascii=False))
        else:
            print(json.dumps({"error": "请使用 --confirm 确认清空"}, ensure_ascii=False))


if __name__ == "__main__":
    main()
