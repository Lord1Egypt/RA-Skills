"""Supported regimes and portable BTC/ETH strategy templates."""

REGIMES = (
    "strong_uptrend",
    "late_uptrend_mixed",
    "range_balanced",
    "event_volatility",
    "distribution_risk",
    "downtrend",
    "recovery_reversal",
)


STRATEGIES = (
    {
        "strategy_id": "wait",
        "eligible_regimes": ("event_volatility", "late_uptrend_mixed", "distribution_risk"),
        "horizon_days": (1, 14),
        "risk_profile": "no_new_exposure",
        "parameter_range": {"reassessment_window_days": (1, 7), "requires_specific_catalyst_or_level": True},
    },
    {
        "strategy_id": "long",
        "eligible_regimes": ("strong_uptrend", "recovery_reversal"),
        "horizon_days": (7, 56),
        "risk_profile": "directional",
        "parameter_range": {"confirmation": "daily_or_4h_trend_and_orderly_funding", "entry_distance_from_support_atr": (0, 1.5), "maximum_horizon_days": 56},
    },
    {
        "strategy_id": "short",
        "eligible_regimes": ("downtrend", "distribution_risk"),
        "horizon_days": (3, 42),
        "risk_profile": "directional",
        "parameter_range": {"confirmation": "daily_or_4h_trend_break_and_non_crowded_funding", "entry_distance_from_resistance_atr": (0, 1.5), "maximum_horizon_days": 42},
    },
    {
        "strategy_id": "call_spread",
        "eligible_regimes": ("strong_uptrend", "late_uptrend_mixed", "recovery_reversal"),
        "horizon_days": (14, 45),
        "risk_profile": "defined_risk",
        "parameter_range": {"option_tenor_days": (21, 60), "long_delta": (.35, .55), "short_delta": (.15, .30), "maximum_surface_fit_rmse_iv_points": 5},
    },
    {
        "strategy_id": "put_spread",
        "eligible_regimes": ("downtrend", "distribution_risk"),
        "horizon_days": (14, 45),
        "risk_profile": "defined_risk",
        "parameter_range": {"option_tenor_days": (21, 60), "long_delta": (-.55, -.35), "short_delta": (-.30, -.15), "maximum_surface_fit_rmse_iv_points": 5},
    },
    {
        "strategy_id": "long_straddle",
        "eligible_regimes": ("event_volatility",),
        "horizon_days": (1, 21),
        "risk_profile": "defined_risk",
        "parameter_range": {"option_tenor_days": (3, 30), "leg_delta_absolute": (.40, .60), "requires_underpriced_implied_move": True, "minimum_catalyst_or_breakout_evidence": True},
    },
    {
        "strategy_id": "long_strangle",
        "eligible_regimes": ("event_volatility",),
        "horizon_days": (1, 30),
        "risk_profile": "defined_risk",
        "parameter_range": {"option_tenor_days": (3, 45), "leg_delta_absolute": (.20, .35), "requires_underpriced_implied_move": True, "minimum_catalyst_or_breakout_evidence": True},
    },
    {
        "strategy_id": "short_straddle",
        "eligible_regimes": ("range_balanced",),
        "horizon_days": (1, 14),
        "risk_profile": "high_risk_defined_loss_required",
        "parameter_range": {"option_tenor_days": (3, 21), "leg_delta_absolute": (.40, .60), "requires_rich_implied_volatility": True, "requires_no_near_catalyst": True, "defined_loss_wrapper": "protective_wings_required"},
    },
    {
        "strategy_id": "short_strangle",
        "eligible_regimes": ("range_balanced",),
        "horizon_days": (1, 21),
        "risk_profile": "high_risk_defined_loss_required",
        "parameter_range": {"option_tenor_days": (7, 30), "leg_delta_absolute": (.10, .25), "requires_rich_implied_volatility": True, "requires_no_near_catalyst": True, "defined_loss_wrapper": "protective_wings_required"},
    },
    {
        "strategy_id": "breakout_capture",
        "eligible_regimes": ("strong_uptrend", "downtrend", "event_volatility", "recovery_reversal"),
        "horizon_days": (1, 21),
        "risk_profile": "conditional",
        "parameter_range": {"confirmation": "4h_or_daily_range_break_and_follow_through", "breakout_buffer_atr": (.1, .5), "minimum_volume_confirmation_ratio": 1, "maximum_horizon_days": 21},
    },
    {
        "strategy_id": "range_grid",
        "eligible_regimes": ("range_balanced",),
        "horizon_days": (1, 14),
        "risk_profile": "conditional",
        "parameter_range": {"requires_defined_range": True, "range_timeframes": ("4h", "1d"), "grid_band_count": (4, 12), "spacing_atr": (.2, .75), "requires_orderly_funding": True, "requires_no_near_catalyst": True},
    },
    {
        "strategy_id": "protective_put",
        "eligible_regimes": ("distribution_risk", "event_volatility", "late_uptrend_mixed"),
        "horizon_days": (7, 45),
        "risk_profile": "hedge",
        "parameter_range": {"option_tenor_days": (7, 60), "put_delta": (-.40, -.20), "coverage_ratio": (.5, 1), "requires_existing_long_exposure": True},
    },
    {
        "strategy_id": "covered_call",
        "eligible_regimes": ("range_balanced", "late_uptrend_mixed"),
        "horizon_days": (14, 45),
        "risk_profile": "capped_upside",
        "parameter_range": {"option_tenor_days": (14, 60), "call_delta": (.15, .30), "coverage_ratio": (.25, 1), "requires_existing_long_exposure": True},
    },
)

STRATEGY_BY_ID = {strategy["strategy_id"]: strategy for strategy in STRATEGIES}
