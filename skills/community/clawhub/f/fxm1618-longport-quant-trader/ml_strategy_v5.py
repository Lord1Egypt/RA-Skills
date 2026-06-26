#!/usr/bin/env python3
"""
港股策略优化 v5 - 机器学习增强
目标：胜率>75% + 年化>50%

使用 ML 模型预测涨跌概率，辅助交易决策
特征：技术指标 + 量价关系 + 动量因子
"""
import yfinance as yf
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score

HK_STOCKS = ["9988.HK", "1211.HK", "9618.HK"]
END_DATE = datetime.now()
START_DATE = END_DATE - timedelta(days=365)  # 1 年数据训练

print("\n" + "=" * 80)
print("🤖 策略优化 v5 - 机器学习增强")
print("=" * 80)
print(f"回测区间：365 天（训练）+ 90 天（测试）")
print(f"股票池：{', '.join(HK_STOCKS)}")
print("=" * 80)

# 下载数据
print("\n📥 下载数据...")
data = {}
for symbol in HK_STOCKS:
    ticker = yf.Ticker(symbol)
    df = ticker.history(start=START_DATE - timedelta(days=60), end=END_DATE)
    if len(df) > 100:
        data[symbol] = df
        print(f"  ✅ {symbol}: {len(df)} 天")

# 特征工程
def create_features(df):
    """创建 ML 特征"""
    df = df.copy()
    
    # 收益率
    df['Return'] = df['Close'].pct_change()
    df['Return_1d'] = df['Return'].shift(1)
    df['Return_3d'] = df['Return'].rolling(3).sum().shift(1)
    df['Return_5d'] = df['Return'].rolling(5).sum().shift(1)
    
    # 均线
    df['MA5'] = df['Close'].rolling(5).mean()
    df['MA10'] = df['Close'].rolling(10).mean()
    df['MA20'] = df['Close'].rolling(20).mean()
    df['MA60'] = df['Close'].rolling(60).mean()
    
    df['Price_vs_MA5'] = df['Close'] / df['MA5'] - 1
    df['Price_vs_MA20'] = df['Close'] / df['MA20'] - 1
    df['Price_vs_MA60'] = df['Close'] / df['MA60'] - 1
    
    df['MA5_vs_MA10'] = df['MA5'] / df['MA10'] - 1
    df['MA5_vs_MA20'] = df['MA5'] / df['MA20'] - 1
    df['MA20_vs_MA60'] = df['MA20'] / df['MA60'] - 1
    
    # RSI
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))
    df['RSI_1d'] = df['RSI'].shift(1)
    
    # 成交量
    df['Vol_MA5'] = df['Volume'].rolling(5).mean()
    df['Vol_Change'] = df['Volume'] / df['Vol_MA5'] - 1
    
    # 波动率
    df['Volatility'] = df['Return'].rolling(20).std()
    
    # 动量
    df['Momentum_5d'] = df['Close'] / df['Close'].shift(5) - 1
    df['Momentum_10d'] = df['Close'] / df['Close'].shift(10) - 1
    
    # 标签：未来 3 天收益>5% 为 1（涨），否则为 0
    df['Future_Return'] = df['Close'].shift(-3) / df['Close'] - 1
    df['Label'] = (df['Future_Return'] > 0.05).astype(int)
    
    return df

# 准备数据
print("\n🔧 特征工程...")
all_features = []
all_labels = []
symbols_data = {}

for symbol, df in data.items():
    df_feat = create_features(df)
    df_feat = df_feat.dropna()
    
    # 分割训练集和测试集（前 365 天训练，后 90 天测试）
    train_len = int(len(df_feat) * 0.75)
    
    feature_cols = ['Return_1d', 'Return_3d', 'Return_5d',
                    'Price_vs_MA5', 'Price_vs_MA20', 'Price_vs_MA60',
                    'MA5_vs_MA10', 'MA5_vs_MA20', 'MA20_vs_MA60',
                    'RSI', 'RSI_1d', 'Vol_Change', 'Volatility',
                    'Momentum_5d', 'Momentum_10d']
    
    X = df_feat[feature_cols].values
    y = df_feat['Label'].values
    
    X_train, X_test = X[:train_len], X[train_len:]
    y_train, y_test = y[:train_len], y[train_len:]
    
    symbols_data[symbol] = {
        'X_train': X_train, 'y_train': y_train,
        'X_test': X_test, 'y_test': y_test,
        'feature_cols': feature_cols,
        'df_feat': df_feat,
        'train_len': train_len
    }
    
    print(f"  ✅ {symbol}: 训练{train_len}天 / 测试{len(df_feat)-train_len}天")

# 训练多个模型
print("\n🤖 训练 ML 模型...")

models = {
    'RandomForest': RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42),
    'LogisticRegression': LogisticRegression(max_iter=1000, random_state=42)
}

model_results = {}

for name, model in models.items():
    print(f"\n📊 {name}:")
    print("-" * 60)
    
    all_preds = []
    all_true = []
    stock_results = {}
    
    for symbol, sdata in symbols_data.items():
        # 训练
        model.fit(sdata['X_train'], sdata['y_train'])
        
        # 预测
        y_pred = model.predict(sdata['X_test'])
        y_true = sdata['y_test']
        
        all_preds.extend(y_pred)
        all_true.extend(y_true)
        
        # 个股绩效
        acc = accuracy_score(y_true, y_pred)
        prec = precision_score(y_true, y_pred, zero_division=0)
        
        stock_results[symbol] = {'acc': acc, 'prec': prec}
        print(f"  {symbol}: 准确率={acc*100:.1f}%, 精确率={prec*100:.1f}%")
    
    # 总体绩效
    overall_acc = accuracy_score(all_true, all_preds)
    overall_prec = precision_score(all_true, all_preds, zero_division=0)
    
    model_results[name] = {
        'accuracy': overall_acc,
        'precision': overall_prec,
        'stock_results': stock_results
    }
    
    print(f"\n  总体：准确率={overall_acc*100:.1f}%, 精确率={overall_prec*100:.1f}%")

# 找出最佳模型
best_model_name = max(model_results, key=lambda x: model_results[x]['precision'])
best_result = model_results[best_model_name]

print("\n" + "=" * 80)
print("🏆 最佳模型")
print("=" * 80)
print(f"模型：{best_model_name}")
print(f"准确率：{best_result['accuracy']*100:.1f}%")
print(f"精确率：{best_result['precision']*100:.1f}%")

# 基于 ML 预测的交易策略回测
print("\n" + "=" * 80)
print("📈 ML 策略回测（测试集 90 天）")
print("=" * 80)

ml_trades = 0
ml_wins = 0
ml_losses = 0
ml_total_return = 0

for symbol, sdata in symbols_data.items():
    df_feat = sdata['df_feat']
    test_start = sdata['train_len']
    df_test = df_feat.iloc[test_start:].copy()
    
    # 获取特征和标签
    feature_cols = sdata['feature_cols']
    X_test = sdata['X_test']
    y_test = sdata['y_test']
    
    # 用最佳模型预测
    best_model = models[best_model_name]
    predictions = best_model.predict(X_test)
    probabilities = best_model.predict_proba(X_test)[:, 1] if hasattr(best_model, 'predict_proba') else predictions
    
    # 交易策略：预测为 1 且概率>0.6 时买入，持有 3 天
    in_position = False
    entry_price = 0
    entry_idx = 0
    
    for idx in range(len(df_test)):
        if predictions[idx] == 1 and probabilities[idx] > 0.6 and not in_position:
            # 买入
            in_position = True
            entry_price = float(df_test.iloc[idx]['Close'])
            entry_idx = idx
        
        # 持有 3 天后卖出
        elif in_position and idx - entry_idx >= 3:
            exit_price = float(df_test.iloc[idx]['Close'])
            pnl = (exit_price - entry_price) / entry_price
            
            ml_trades += 1
            ml_total_return += pnl
            if pnl > 0:
                ml_wins += 1
            else:
                ml_losses += 1
            
            in_position = False
    
    print(f"\n{symbol}:")
    print(f"  交易数：{ml_trades} 次")
    print(f"  胜率：{(ml_wins/ml_trades*100) if ml_trades>0 else 0:.1f}%")
    print(f"  收益：{ml_total_return*100:.2f}%")

# 总体 ML 策略绩效
ml_win_rate = (ml_wins / ml_trades * 100) if ml_trades > 0 else 0
ml_annual_return = (1 + ml_total_return) ** (365/90) - 1 if ml_trades > 0 else 0

print("\n" + "=" * 80)
print("📊 ML 策略总体绩效")
print("=" * 80)
print(f"交易数：{ml_trades} 次")
print(f"胜率：{ml_win_rate:.1f}%")
print(f"总收益：{ml_total_return*100:.2f}%")
print(f"年化收益：{ml_annual_return*100:.2f}%")

# 距离目标
print("\n" + "=" * 80)
print("🎯 距离目标")
print("=" * 80)
target_wr = 75
target_ret = 50

wr_gap = target_wr - ml_win_rate
ret_gap = target_ret - ml_annual_return*100

print(f"胜率：{ml_win_rate:.1f}% / {target_wr}% (差距：{wr_gap:.1f}%)")
print(f"年化收益：{ml_annual_return*100:.2f}% / {target_ret}% (差距：{ret_gap:.2f}%)")

if ml_win_rate >= target_wr and ml_annual_return*100 >= target_ret:
    print("\n✅🎉 目标达成！")
else:
    print("\n⚠️ 继续优化...")

print("\n" + "=" * 80)
print("✅ ML 策略测试完成")
print("=" * 80)
