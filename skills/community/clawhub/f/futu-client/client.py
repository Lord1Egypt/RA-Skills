"""
Futu API Client - A convenient wrapper for Futu OpenAPI trading.

This client provides methods for querying positions, account info,
placing orders, and more using Futu OpenAPI.
Requires FutuOpenD to be running on localhost:11111.
"""

from typing import Optional, List, Dict, Any
import pandas as pd

from futu import (
    OpenSecTradeContext,
    OpenQuoteContext,
    TrdEnv,
    TrdMarket,
    SecurityFirm,
    TrdSide,
    OrderType,
    PositionSide,
    SubType,
)


class FutuClient:
    """
    A client for Futu OpenAPI trading and query.
    
    Requires FutuOpenD to be running on 127.0.0.1:11111
    
    Example usage:
        client = FutuClient()  # Default: HK market
        
        # Or specify market: 'HK', 'US', 'CN'
        client = FutuClient(market='US')
        
        # Get positions
        positions = client.get_positions()
        
        # Get account info
        account = client.get_account_info()
        
        # Place order
        result = client.place_order(price=100.0, qty=100, code="HK.00700", trd_side=TrdSide.BUY)
        
        # Get order list
        orders = client.get_orders()
        
        client.close()
    """
    
    def __init__(self, host: str = "127.0.0.1", port: int = 11111, market: str = "HK"):
        """
        Initialize the Futu client.
        
        Args:
            host: FutuOpenD host (default: 127.0.0.1)
            port: FutuOpenD port (default: 11111)
            market: Trading market - 'HK', 'US', 'CN' (default: 'HK')
        """
        self.host = host
        self.port = port
        self.market = market.upper()
        
        # Map market string to TrdMarket
        market_map = {
            'HK': TrdMarket.HK,
            'US': TrdMarket.US,
            'CN': TrdMarket.CN,
        }
        self.trd_market = market_map.get(self.market, TrdMarket.HK)
        
        self.trd_ctx = None
        self.quote_ctx = None
    
    def _get_trade_context(self) -> OpenSecTradeContext:
        """Get or create trade context."""
        if self.trd_ctx is None:
            self.trd_ctx = OpenSecTradeContext(
                host=self.host,
                port=self.port,
                security_firm=SecurityFirm.FUTUSECURITIES,
                filter_trdmarket=self.trd_market
            )
        return self.trd_ctx
    
    def _get_quote_context(self) -> OpenQuoteContext:
        """Get or create quote context."""
        if self.quote_ctx is None:
            self.quote_ctx = OpenQuoteContext(host=self.host, port=self.port)
        return self.quote_ctx
    
    def get_positions(self, trd_env: TrdEnv = TrdEnv.REAL) -> pd.DataFrame:
        """
        Get current positions.
        
        Args:
            trd_env: Trading environment (TrdEnv.REAL or TrdEnv.SIMULATE)
            
        Returns:
            DataFrame with position data including:
            - code: stock code
            - stock_name: stock name
            - qty: position quantity
            - can_sell_qty: available to sell
            - cost_price: cost price
            - nominal_price: current price
            - pl_ratio: profit/loss ratio
            - currency: currency
        """
        ctx = self._get_trade_context()
        ret, data = ctx.position_list_query(trd_env=trd_env)
        if ret != 0:
            raise Exception(f"Failed to get positions: {data}")
        return data
    
    def get_account_info(self, trd_env: TrdEnv = TrdEnv.REAL) -> Dict[str, Any]:
        """
        Get account information.
        
        Args:
            trd_env: Trading environment
            
        Returns:
            Dictionary with account data including:
            - total_assets: total assets
            - cash: available cash
            - power: buying power
            - market_val: position market value
            - currency: account currency
        """
        ctx = self._get_trade_context()
        ret, data = ctx.accinfo_query(trd_env=trd_env)
        if ret != 0:
            raise Exception(f"Failed to get account info: {data}")
        return data.iloc[0].to_dict()
    
    def get_today_deals(self, trd_env: TrdEnv = TrdEnv.REAL) -> pd.DataFrame:
        """
        Get today's executed trades.
        
        Args:
            trd_env: Trading environment
            
        Returns:
            DataFrame with deal records
        """
        ctx = self._get_trade_context()
        ret, data = ctx.deal_list_query(trd_env=trd_env)
        if ret != 0:
            raise Exception(f"Failed to get deals: {data}")
        return data
    
    def get_orders(self, trd_env: TrdEnv = TrdEnv.REAL) -> pd.DataFrame:
        """
        Get order list.
        
        Args:
            trd_env: Trading environment
            
        Returns:
            DataFrame with order records
        """
        ctx = self._get_trade_context()
        ret, data = ctx.order_list_query(trd_env=trd_env)
        if ret != 0:
            raise Exception(f"Failed to get orders: {data}")
        return data
    
    def place_order(
        self,
        price: float,
        qty: int,
        code: str,
        trd_side: TrdSide = TrdSide.BUY,
        order_type: OrderType = OrderType.NORMAL,
        trd_env: TrdEnv = TrdEnv.REAL
    ) -> Dict[str, Any]:
        """
        Place an order.
        
        Args:
            price: Order price
            qty: Order quantity
            code: Stock code (e.g., "HK.00700", "US.AAPL")
            trd_side: Trade side (TrdSide.BUY or TrdSide.SELL)
            order_type: Order type (OrderType.NORMAL, etc.)
            trd_env: Trading environment
            
        Returns:
            Dictionary with order result
        """
        ctx = self._get_trade_context()
        ret, data = ctx.place_order(
            price=price,
            qty=qty,
            code=code,
            trd_side=trd_side,
            order_type=order_type,
            trd_env=trd_env
        )
        if ret != 0:
            raise Exception(f"Failed to place order: {data}")
        return data.iloc[0].to_dict()
    
    def modify_order(
        self,
        order_id: int,
        price: Optional[float] = None,
        qty: Optional[int] = None,
        trd_env: TrdEnv = TrdEnv.REAL
    ) -> Dict[str, Any]:
        """
        Modify or cancel an order.
        
        Args:
            order_id: Order ID to modify
            price: New price (None to keep original)
            qty: New quantity (None to keep original)
            trd_env: Trading environment
            
        Returns:
            Dictionary with modification result
        """
        ctx = self._get_trade_context()
        ret, data = ctx.modify_order(
            order_id=order_id,
            price=price,
            qty=qty,
            trd_env=trd_env
        )
        if ret != 0:
            raise Exception(f"Failed to modify order: {data}")
        return data.iloc[0].to_dict()
    
    def unlock_trade(self, password: str, trd_env: TrdEnv = TrdEnv.REAL) -> bool:
        """
        Unlock trading with password.
        
        Args:
            password: Trading password
            trd_env: Trading environment
            
        Returns:
            True if successful
        """
        ctx = self._get_trade_context()
        ret, data = ctx.unlock_trade(password=password, trd_env=trd_env)
        return ret == 0
    
    def get_quote(self, code: str) -> Dict[str, Any]:
        """
        Get real-time quote for a stock.
        
        Args:
            code: Stock code (e.g., "HK.00700", "US.AAPL")
            
        Returns:
            Dictionary with quote data
        """
        ctx = self._get_quote_context()
        # Subscribe first
        ctx.subscribe(code, [SubType.QUOTE])
        ret, data = ctx.get_stock_quote(code)
        if ret != 0:
            raise Exception(f"Failed to get quote: {data}")
        return data.iloc[0].to_dict()
    
    def get_market_snapshot(self, codes: List[str]) -> pd.DataFrame:
        """
        Get market snapshot for multiple stocks.
        
        Args:
            codes: List of stock codes
            
        Returns:
            DataFrame with market snapshot
        """
        ctx = self._get_quote_context()
        ret, data = ctx.get_market_snapshot(codes)
        if ret != 0:
            raise Exception(f"Failed to get snapshot: {data}")
        return data
    
    def get_history_orders(
        self,
        trd_env: TrdEnv = TrdEnv.REAL,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> pd.DataFrame:
        """
        Get historical order list.
        
        Args:
            trd_env: Trading environment
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
            
        Returns:
            DataFrame with historical orders
        """
        ctx = self._get_trade_context()
        ret, data = ctx.history_order_list_query(
            trd_env=trd_env,
            start_date=start_date,
            end_date=end_date
        )
        if ret != 0:
            raise Exception(f"Failed to get history orders: {data}")
        return data
    
    def get_history_deals(
        self,
        trd_env: TrdEnv = TrdEnv.REAL,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> pd.DataFrame:
        """
        Get historical deal list.
        
        Args:
            trd_env: Trading environment
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
            
        Returns:
            DataFrame with historical deals
        """
        ctx = self._get_trade_context()
        ret, data = ctx.history_deal_list_query(
            trd_env=trd_env,
            start_date=start_date,
            end_date=end_date
        )
        if ret != 0:
            raise Exception(f"Failed to get history deals: {data}")
        return data
    
    def get_max_tradable_qty(
        self,
        code: str,
        price: float,
        trd_env: TrdEnv = TrdEnv.REAL
    ) -> Dict[str, Any]:
        """
        Get maximum tradable quantity for a given price.
        
        Args:
            code: Stock code
            price: Target price
            trd_env: Trading environment
            
        Returns:
            Dictionary with max quantity info
        """
        ctx = self._get_trade_context()
        ret, data = ctx.acctradinginfo_query(
            code=code,
            price=price,
            trd_env=trd_env
        )
        if ret != 0:
            raise Exception(f"Failed to get max tradable qty: {data}")
        return data.iloc[0].to_dict()
    
    def get_watchlist(self, group_name: str = "全部") -> pd.DataFrame:
        """
        Get user's watchlist (self-selected stocks).
        
        Args:
            group_name: Watchlist group name (default: "全部")
                        Common names: "全部", "港股", "美股", "沪深"
            
        Returns:
            DataFrame with watchlist stocks including:
            - code: stock code
            - name: stock name
            - lot_size: lot size
            - stock_type: stock type
        """
        ctx = self._get_quote_context()
        ret, data = ctx.get_user_security(group_name)
        if ret != 0:
            raise Exception(f"Failed to get watchlist: {data}")
        return data
    
    def get_all_watchlists(self) -> Dict[str, pd.DataFrame]:
        """
        Get all watchlist groups.
        
        Returns:
            Dictionary mapping group names to DataFrames
        """
        ctx = self._get_quote_context()
        groups_to_try = ["全部", "港股", "美股", "沪深", "All", "HK", "US", "CN"]
        result = {}
        for name in groups_to_try:
            try:
                ret, data = ctx.get_user_security(name)
                if ret == 0 and len(data) > 0:
                    result[name] = data
            except:
                pass
        return result
    
    def close(self):
        """Close all contexts."""
        if self.trd_ctx:
            self.trd_ctx.close()
            self.trd_ctx = None
        if self.quote_ctx:
            self.quote_ctx.close()
            self.quote_ctx = None
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
