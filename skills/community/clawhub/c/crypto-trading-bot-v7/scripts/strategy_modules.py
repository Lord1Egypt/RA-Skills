1. 市场状态识别模块
python
class MarketStateDetector:
    """
    市场状态识别器
    基于ADX和价格相对于均线的位置判断趋势/震荡
    """
    def __init__(self, adx_period=14, adx_threshold=25, ma_period=50):
        self.adx_period = adx_period
        self.adx_threshold = adx_threshold   # ADX高于此值为趋势，低于为震荡
        self.ma_period = ma_period

    def compute_adx(self, high, low, close):
        """计算ADX序列"""
        # 计算+DM和-DM
        up_move = high.diff()
        down_move = -low.diff()
        plus_dm = up_move.where((up_move > down_move) & (up_move > 0), 0.0)
        minus_dm = down_move.where((down_move > up_move) & (down_move > 0), 0.0)
        # 计算真实波幅TR
        tr = np.maximum(high - low, np.abs(high - close.shift(1)), np.abs(low - close.shift(1)))
        # 平滑
        atr = tr.rolling(self.adx_period).mean()
        plus_di = 100 * plus_dm.rolling(self.adx_period).mean() / atr
        minus_di = 100 * minus_dm.rolling(self.adx_period).mean() / atr
        dx = 100 * np.abs(plus_di - minus_di) / (plus_di + minus_di)
        adx = dx.rolling(self.adx_period).mean()
        return adx

    def is_trending(self, adx):
        """判断是否处于趋势行情"""
        return adx > self.adx_threshold

    def get_trend_direction(self, close, ma):
        """获取趋势方向（基于价格与均线的关系）"""
        if close > ma:
            return 'bullish'
        elif close < ma:
            return 'bearish'
        else:
            return 'neutral'

    def update(self, high, low, close):
        """更新市场状态，返回状态字典"""
        adx = self.compute_adx(high, low, close).iloc[-1]
        ma = close.rolling(self.ma_period).mean().iloc[-1]
        trending = self.is_trending(adx)
        direction = self.get_trend_direction(close.iloc[-1], ma) if trending else 'neutral'
        return {
            'adx': adx,
            'trending': trending,
            'direction': direction,
            'ma': ma
        }
2. 策略池（示例策略）
我们需要定义策略的接口。每个策略应包含：

name：策略名称

generate_signal：根据当前数据返回信号（1=做多，-1=做空，0=无信号）

可选：策略自身需要的参数

这里给出两个示例策略：

2.1 趋势跟踪策略（基于Supertrend）
python
class SupertrendStrategy:
    """
    基于Supertrend的趋势跟踪策略
    """
    def __init__(self, period=10, multiplier=3):
        self.period = period
        self.multiplier = multiplier
        self.name = "Supertrend"

    def compute_supertrend(self, high, low, close):
        """计算Supertrend指标"""
        # 计算ATR
        tr = np.maximum(high - low, np.abs(high - close.shift(1)), np.abs(low - close.shift(1)))
        atr = tr.rolling(self.period).mean()
        # 计算基本上下轨
        hl_avg = (high + low) / 2
        upper_band = hl_avg + self.multiplier * atr
        lower_band = hl_avg - self.multiplier * atr
        # 初始化Supertrend
        supertrend = pd.Series(index=close.index, dtype=float)
        trend = pd.Series(index=close.index, dtype=int)  # 1=上升趋势，-1=下降趋势
        for i in range(self.period, len(close)):
            if i == self.period:
                supertrend.iloc[i] = upper_band.iloc[i]
                trend.iloc[i] = 1 if close.iloc[i] > supertrend.iloc[i] else -1
            else:
                if close.iloc[i] > upper_band.iloc[i-1]:
                    trend.iloc[i] = 1
                elif close.iloc[i] < lower_band.iloc[i-1]:
                    trend.iloc[i] = -1
                else:
                    trend.iloc[i] = trend.iloc[i-1]
                # 更新Supertrend线
                if trend.iloc[i] == 1:
                    supertrend.iloc[i] = lower_band.iloc[i] if trend.iloc[i-1] == -1 else max(lower_band.iloc[i], supertrend.iloc[i-1])
                else:
                    supertrend.iloc[i] = upper_band.iloc[i] if trend.iloc[i-1] == 1 else min(upper_band.iloc[i], supertrend.iloc[i-1])
        return supertrend, trend

    def generate_signal(self, high, low, close):
        """生成信号：1=做多，-1=做空，0=无"""
        _, trend = self.compute_supertrend(high, low, close)
        current_trend = trend.iloc[-1]
        # 仅当趋势发生变化时产生信号（简单示例：可用趋势方向直接作为持仓信号）
        if current_trend == 1:
            return 1
        elif current_trend == -1:
            return -1
        else:
            return 0
2.2 均值回归策略（基于RSI）
python
class MeanReversionStrategy:
    """
    基于RSI的均值回归策略，在超买超卖区域反向开仓
    """
    def __init__(self, rsi_period=14, oversold=30, overbought=70):
        self.rsi_period = rsi_period
        self.oversold = oversold
        self.overbought = overbought
        self.name = "MeanReversion"

    def compute_rsi(self, close):
        delta = close.diff()
        gain = delta.where(delta > 0, 0.0)
        loss = -delta.where(delta < 0, 0.0)
        avg_gain = gain.rolling(self.rsi_period).mean()
        avg_loss = loss.rolling(self.rsi_period).mean()
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        return rsi

    def generate_signal(self, high, low, close):
        rsi = self.compute_rsi(close).iloc[-1]
        if rsi < self.oversold:
            return 1   # 超卖做多
        elif rsi > self.overbought:
            return -1  # 超买做空
        else:
            return 0
3. 策略选择器
策略选择器根据市场状态从策略池中选择一个策略。

python
class StrategySelector:
    """
    策略选择器：根据市场状态选择最适合的策略
    """
    def __init__(self, market_state_detector, strategies):
        """
        market_state_detector: MarketStateDetector实例
        strategies: 字典，键为策略名称，值为策略实例
        """
        self.detector = market_state_detector
        self.strategies = strategies

    def select_strategy(self, high, low, close):
        """根据当前市场状态选择策略"""
        state = self.detector.update(high, low, close)
        # 趋势行情 -> 选择趋势策略（这里假设Supertrend是趋势策略）
        if state['trending']:
            # 根据趋势方向，可以进一步选择做多或做空的策略
            # 这里简单返回趋势策略实例
            return self.strategies.get('Supertrend', None)
        else:
            # 震荡行情 -> 选择均值回归策略
            return self.strategies.get('MeanReversion', None)
4. 多策略组合框架
我们可以实现两种组合方式：

信号融合：综合多个策略的信号，例如取多数投票或加权平均。

资金分配：同时运行多个策略，每个策略独立开仓，按一定比例分配资金。

这里提供一种简单的加权信号融合方式，并可选资金分配。

4.1 信号融合器
python
class SignalFusion:
    """
    信号融合器：综合多个策略的信号，生成最终信号
    """
    def __init__(self, strategies, weights=None):
        """
        strategies: 策略实例列表
        weights: 各策略权重列表（默认为等权）
        """
        self.strategies = strategies
        self.weights = weights if weights else [1.0/len(strategies)] * len(strategies)

    def generate_signal(self, high, low, close):
        signals = []
        for strat in self.strategies:
            sig = strat.generate_signal(high, low, close)
            signals.append(sig)
        # 加权平均（信号值在-1到1之间）
        weighted_signal = np.dot(signals, self.weights)
        # 阈值判断，例如超过0.3做多，低于-0.3做空，否则无信号
        if weighted_signal > 0.3:
            return 1
        elif weighted_signal < -0.3:
            return -1
        else:
            return 0
4.2 资金分配管理器
如果要独立运行多个策略并分别分配资金，可以这样设计：

python
class PortfolioAllocator:
    """
    资金分配管理器：将总资金按比例分配给多个子策略，每个子策略独立运行
    """
    def __init__(self, strategies, allocations, risk_manager):
        """
        strategies: 策略实例列表
        allocations: 各策略资金占比列表（总和应为1）
        risk_manager: 风控管理器实例
        """
        self.strategies = strategies
        self.allocations = allocations
        self.risk_manager = risk_manager
        self.sub_portfolios = {strat.name: {'equity': 0, 'position': 0} for strat in strategies}

    def update_total_equity(self, total_equity):
        """更新各子账户资金（按比例分配）"""
        for i, strat in enumerate(self.strategies):
            self.sub_portfolios[strat.name]['equity'] = total_equity * self.allocations[i]

    def generate_signals(self, high, low, close, total_equity):
        """为每个子策略生成信号并计算仓位（模拟开仓）"""
        self.update_total_equity(total_equity)
        signals = []
        for i, strat in enumerate(self.strategies):
            sig = strat.generate_signal(high, low, close)
            if sig != 0:
                # 获取该策略对应的风控参数（可针对策略个性化）
                atr = self.risk_manager.compute_atr(high, low, close).iloc[-1]
                atr_history = self.risk_manager.compute_atr(high, low, close).dropna().values
                # 这里简化：使用固定入场价（实际应为信号触发价格）
                entry_price = close.iloc[-1]
                stop_price, take_profit = self.risk_manager.get_stop_loss_and_take_profit(
                    entry_price, 'long' if sig == 1 else 'short', atr, atr_history
                )
                pos_size = self.risk_manager.calculate_position_size(
                    self.sub_portfolios[strat.name]['equity'], entry_price, stop_price
                )
                signals.append({
                    'strategy': strat.name,
                    'signal': sig,
                    'position_size': pos_size,
                    'entry_price': entry_price,
                    'stop_loss': stop_price,
                    'take_profit': take_profit
                })
        return signals
5. 整合示例
最后，我们可以将所有模块整合到一个主循环中：

python
# 初始化组件
risk_mgr = DynamicRiskManager(risk_per_trade=0.015,
                              base_atr_mult=1.5,
                              atr_percentile_high=90,
                              enable_trailing_stop=True)

market_detector = MarketStateDetector(adx_period=14, adx_threshold=25, ma_period=50)
trend_strategy = SupertrendStrategy()
meanrev_strategy = MeanReversionStrategy()

# 策略选择器
selector = StrategySelector(market_detector, {'Supertrend': trend_strategy, 'MeanReversion': meanrev_strategy})

# 或者使用多策略组合（信号融合）
fusion = SignalFusion([trend_strategy, meanrev_strategy], weights=[0.6, 0.4])

# 或者使用资金分配
allocator = PortfolioAllocator([trend_strategy, meanrev_strategy], allocations=[0.6, 0.4], risk_manager=risk_mgr)

# 主循环示例
for i in range(len(df)):
    # 获取最新数据切片
    data_slice = df.iloc[:i+1]
    high = data_slice['high']
    low = data_slice['low']
    close = data_slice['close']
    # 方式1：策略选择器
    selected_strategy = selector.select_strategy(high, low, close)
    if selected_strategy:
        signal = selected_strategy.generate_signal(high, low, close)
        # 执行开仓及风控逻辑...
    # 方式2：信号融合
    fused_signal = fusion.generate_signal(high, low, close)
    # 方式3：资金分配
    sub_signals = allocator.generate_signals(high, low, close, current_equity)
    # 根据sub_signals执行多个子策略的独立开仓...
你可以根据自己的回测框架选择合适的方式。以上模块均设计为可插拔，方便集成到现有策略中