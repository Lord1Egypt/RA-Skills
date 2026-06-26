# Known Use Cases (KUC)

Total: **88**

## `KUC-101`
**Source**: `notebooks/finutils/FINCALENDAR_IntroductionToUsingCalendars.ipynb`

Determining business days and holidays for different countries to correctly schedule financial transactions and settlements.

## `KUC-102`
**Source**: `notebooks/finutils/FINDATES_TestingDateInternals.ipynb`

Testing internal date representation and Excel date serial number conversion for financial date calculations.

## `KUC-103`
**Source**: `notebooks/finutils/FINDATE_CreatingAndManipulatingFinDates.ipynb`

Creating and manipulating financial dates including adding days, months, tenors, and handling weekends for trade scheduling.

## `KUC-104`
**Source**: `notebooks/finutils/FINDAYCOUNT_Introduction.ipynb`

Calculating year fractions and day counts using various conventions (ACT/360, ACT/365, 30/360) for interest accrual calculations.

## `KUC-105`
**Source**: `notebooks/finutils/FINSCHEDULE_ExamplesOfScheduleGeneration.ipynb`

Generating payment schedules for bonds, swaps, and other fixed income instruments with proper date adjustments.

## `KUC-106`
**Source**: `notebooks/finutils/TENSIONSPLINE_Example.ipynb`

Using tension spline interpolation for smooth curve fitting with adjustable tension parameter.

## `KUC-107`
**Source**: `notebooks/market/curves/FINDISCOUNTCURVEFLAT_ExaminationOfDiscountCurveFlat.ipynb`

Analyzing discount factors and zero rates using a flat discount curve with different compounding frequencies.

## `KUC-108`
**Source**: `notebooks/market/curves/FINDISCOUNTCURVENSS_IntroductionToTheNelsonSiegelSvenssonCurve.ipynb`

Fitting yield curves using the Nelson-Siegel-Svensson parametric model for interest rate surface estimation.

## `KUC-109`
**Source**: `notebooks/market/curves/FINDISCOUNTCURVENS_ExaminingTheNelsonSiegelCurve.ipynb`

Analyzing the Nelson-Siegel model factor loadings and curve fitting for yield curve construction.

## `KUC-110`
**Source**: `notebooks/market/curves/FINDISCOUNTCURVEPOLY_SimpleAnalysis.ipynb`

Fitting discount curves using polynomial functions for yield curve construction and forward rate analysis.

## `KUC-111`
**Source**: `notebooks/market/curves/FINDISCOUNTCURVEZERO_ConvertZeroCurveToDiscountCurve.ipynb`

Converting zero rate curves to discount factor curves for bond and derivatives pricing.

## `KUC-112`
**Source**: `notebooks/market/curves/FINDISCOUNTCURVE_AnalysisOfInterpolationSchemes.ipynb`

Comparing different interpolation methods (linear, cubic spline) for discount curve construction.

## `KUC-113`
**Source**: `notebooks/market/curves/FINDISCOUNTCURVE_Introduction.ipynb`

Introduction to discount curve construction and calculating forward rates, swap rates from the curve.

## `KUC-114`
**Source**: `notebooks/market/curves/FINDISCOUNTCURVE_PieceWiseFlatOverNightForwardRateDiscountCurve.ipynb`

Building discount curves using piecewise flat overnight forward rates with bump analysis for risk management.

## `KUC-115`
**Source**: `notebooks/market/volatility/EquityVolSurfaceConstructionSVI.ipynb`

Constructing equity implied volatility surfaces using the SVI (Stochastic Volatility Inspired) parameterization.

## `KUC-116`
**Source**: `notebooks/market/volatility/FXVolSurfaceConstructionPartOne.ipynb`

Building FX implied volatility surfaces from market quotes using various volatility function types.

## `KUC-117`
**Source**: `notebooks/market/volatility/FXVolSurfaceConstructionPartTwo.ipynb`

Extended FX volatility surface construction with 10-delta and 25-delta quotes.

## `KUC-118`
**Source**: `notebooks/market/volatility/FXVolSurfaceConstructionPartThree.ipynb`

Advanced FX volatility surface construction with multiple tenors and full delta coverage.

## `KUC-119`
**Source**: `notebooks/market/volatility/SimpleBuildFXVolatilitySurface25Delta.ipynb`

Building a simple FX volatility surface using 25-delta risk reversals and strangles.

## `KUC-120`
**Source**: `notebooks/models/CHOLESKY CHECK.ipynb`

Validating Cholesky decomposition for generating correlated random variables in Monte Carlo simulations.

## `KUC-121`
**Source**: `notebooks/models/FINGBMPROCESS_generatePaths.ipynb`

Generating Geometric Brownian Motion paths for asset price simulation in Monte Carlo pricing.

## `KUC-122`
**Source**: `notebooks/models/FINITE_DIFFERENCE.ipynb`

Pricing options using finite difference methods (explicit, implicit, Crank-Nicolson) for Black-Scholes PDE.

## `KUC-123`
**Source**: `notebooks/models/FINITE_DIFFERENCE_PSOR.ipynb`

Using Projected Successive Over-Relaxation (PSOR) to solve finite difference equations for option pricing.

## `KUC-124`
**Source**: `notebooks/models/FINMODEL_GAUSSIANCOPULA_PortfolioLossDistributionBuilder.ipynb`

Building portfolio loss distributions using one-factor Gaussian copula model for credit risk analysis.

## `KUC-125`
**Source**: `notebooks/models/FINMODEL_SABRSHIFTED_InterestRates.ipynb`

Pricing interest rate swaptions using the shifted SABR model to capture volatility smile.

## `KUC-126`
**Source**: `notebooks/models/FINMODEL_SABRSHIFTED_VolatilitySmile.ipynb`

Analyzing volatility smiles using the shifted SABR model for low-rate environments.

## `KUC-127`
**Source**: `notebooks/models/FINMODEL_SABR_InterestRates.ipynb`

Implementing and analyzing the SABR stochastic volatility model for interest rate derivatives.

## `KUC-128`
**Source**: `notebooks/models/FINVOLFUNCTIONS_SSVI_MODEL.ipynb`

Analyzing the Surface SVI (SSVI) parameterization for volatility surface construction and arbitrage-free interpolation.

## `KUC-129`
**Source**: `notebooks/models/MERTON_CREDIT_MODEL.ipynb`

Structural credit risk modeling using Merton's firm value model to calculate default probability and credit spreads.

## `KUC-130`
**Source**: `notebooks/products/bonds/FINANNUITY_Valuation.ipynb`

Valuing bond annuity schedules and calculating clean/dirty prices using discount curves.

## `KUC-131`
**Source**: `notebooks/products/bonds/FINBONDCONVERTIBLE_ComparisonWithQLExample.ipynb`

Validating convertible bond pricing against QuantLib reference implementations.

## `KUC-132`
**Source**: `notebooks/products/bonds/FINBONDCONVERTIBLE_ValuationAndConvergenceTest.ipynb`

Testing convergence of convertible bond Monte Carlo valuation with varying step sizes.

## `KUC-133`
**Source**: `notebooks/products/bonds/FINBONDEMBEDDEDOPTION_Valuation.ipynb`

Valuing callable and putable bonds using interest rate tree models (Hull-White, Black-Karasinski).

## `KUC-134`
**Source**: `notebooks/products/bonds/FINBONDFRN_CitigroupExample.ipynb`

Pricing floating rate notes (FRNs) and calculating discount margin, duration, and convexity.

## `KUC-135`
**Source**: `notebooks/products/bonds/FINBONDFUTURES_ExampleContracts.ipynb`

Analyzing bond futures contracts and calculating cheapest-to-deliver and invoice prices.

## `KUC-136`
**Source**: `notebooks/products/bonds/FINBONDMARKET_DatabaseOfConventions.ipynb`

Accessing standard bond market conventions including day count, frequency, settlement days for different countries.

## `KUC-137`
**Source**: `notebooks/products/bonds/FINBONDMORTGAGE_SimpleCalculator.ipynb`

Calculating mortgage repayment schedules including interest-only and repayment modes.

## `KUC-138`
**Source**: `notebooks/products/bonds/FINBONDOPTION_All_Models_Valuation_Analysis.ipynb`

Valuing bond options (European and American) using various short rate models.

## `KUC-139`
**Source**: `notebooks/products/bonds/FINBONDOPTION_BK_ModelValuationAnalysis.ipynb`

Pricing bond options using the Black-Karasinski interest rate model.

## `KUC-140`
**Source**: `notebooks/products/bonds/FINBONDOPTION_HW_EXAMPLE_MATCH_DERIVA_GEN.ipynb`

Valuing bond options using Hull-White model validated against DerivaGem.

## `KUC-141`
**Source**: `notebooks/products/bonds/FINBONDOPTION_HW_Model_Jamshidian.ipynb`

Pricing European bond options using Hull-White model with Jamshidian decomposition.

## `KUC-142`
**Source**: `notebooks/products/bonds/FINBONDOPTION_Tree_Convergence_With_Volatility.ipynb`

Analyzing convergence of lattice tree methods for bond option pricing with varying volatility.

## `KUC-143`
**Source**: `notebooks/products/bonds/FINBONDOPTION_Tree_Convergence_Zero_Vol.ipynb`

Testing tree convergence for bond options in zero volatility (lognormal) limiting case.

## `KUC-144`
**Source**: `notebooks/products/bonds/FINBONDYIELDCURVES_FittingExample.ipynb`

Fitting yield curves to bond prices using polynomial regression.

## `KUC-145`
**Source**: `notebooks/products/bonds/FINBONDYIELDCURVE_FittingToAswAndZSpreads.ipynb`

Fitting bond yield curves to asset swap spreads and Z-spreads.

## `KUC-146`
**Source**: `notebooks/products/bonds/FINBONDYIELDCURVE_FittingToBondMarketPrices.ipynb`

Fitting yield curves directly to observable bond market prices.

## `KUC-147`
**Source**: `notebooks/products/bonds/FINBONDZEROCURVE_BootstrapOutstandingBonds.ipynb`

Bootstrapping zero coupon curves from outstanding bond prices.

## `KUC-148`
**Source**: `notebooks/products/bonds/FINBOND_CalculateOptionAdjustedSpread.ipynb`

Calculating option-adjusted spread (OAS) for callable bonds.

## `KUC-149`
**Source**: `notebooks/products/bonds/FINBOND_CalculatePriceUsingSurvivalCurve.ipynb`

Calculating bond prices using survival (credit) curves accounting for default risk.

## `KUC-150`
**Source**: `notebooks/products/bonds/FINBOND_CalculatingTheAssetSwapSpread.ipynb`

Calculating asset swap spreads for bonds relative to LIBOR.

## `KUC-151`
**Source**: `notebooks/products/bonds/FINBOND_ComparisonWithQLExample.ipynb`

Validating bond pricing implementation against QuantLib reference.

## `KUC-152`
**Source**: `notebooks/products/bonds/FINBOND_DiscountingBondCashflowsFinDiscountCurve.ipynb`

Calculating bond prices by discounting cash flows using a flat discount curve.

## `KUC-153`
**Source**: `notebooks/products/bonds/FINBOND_ExampleAppleCorp.ipynb`

Full analysis of Apple corporate bond including yield, duration, convexity, and accrued interest.

## `KUC-154`
**Source**: `notebooks/products/bonds/FINBOND_ExampleUSTreasury_CUSIP_91282CFX4.ipynb`

Valuing US Treasury bonds with proper conventions and calculating yields.

## `KUC-155`
**Source**: `notebooks/products/bonds/FINBOND_Key_Rate_Durations_Example.ipynb`

Calculating key rate durations for bond portfolio yield curve sensitivity analysis.

## `KUC-156`
**Source**: `notebooks/products/credit/FINCDSBASKET_ValuationModelComparison.ipynb`

Comparing different valuation models for CDS baskets and basket default swaps.

## `KUC-157`
**Source**: `notebooks/products/credit/FINCDSCURVE_BuildingASurvivalCurve.ipynb`

Building credit survival curves from CDS term structures for credit derivative pricing.

## `KUC-158`
**Source**: `notebooks/products/credit/FINCDSINDEXOPTION_CompareValuationApproaches.ipynb`

Comparing different approaches for valuing CDS index options.

## `KUC-159`
**Source**: `notebooks/products/credit/FINCDSINDEX_ValuingCDSIndex.ipynb`

Valuing credit default swap indices (CDX, iTraxx) and calculating par spreads.

## `KUC-160`
**Source**: `notebooks/products/credit/FINCDSOPTION_ValuingCDSOption.ipynb`

Valuing options on credit default swaps including sensitivity analysis.

## `KUC-161`
**Source**: `notebooks/products/credit/FINCDSTRANCHE_CalculatingFairSpread.ipynb`

Calculating fair spreads for CDS index tranches with different attachment/detachment points.

## `KUC-162`
**Source**: `notebooks/products/credit/FINCDS_ComparisonWithMarkitCDSModel.ipynb`

Validating CDS valuation against Markit CDS model reference implementation.

## `KUC-163`
**Source**: `notebooks/products/credit/FINCDS_CreatingAndValuingACDS.ipynb`

Creating and valuing credit default swaps including par spread and PV calculations.

## `KUC-164`
**Source**: `notebooks/products/credit/FINCDS_CreatingAndValuingACDSFlatCurves.ipynb`

CDS valuation using simplified flat discount and survival curves.

## `KUC-165`
**Source**: `notebooks/products/credit/FINCDS_ForwardAndBackward.ipynb`

Understanding CDS cash flow generation using forward vs backward date generation rules.

## `KUC-166`
**Source**: `notebooks/products/equity/EQUITY_AMERICANOPTION_BARONE_ADESI_WHALEY_APPROX.ipynb`

Pricing American options using Barone-Adesi Whaley approximation method.

## `KUC-167`
**Source**: `notebooks/products/equity/EQUITY_AMERICANOPTION_BJERKSUND_STENSLAND_APPROX.ipynb`

Pricing American options using Bjerksund-Stensland approximation for call-put parity.

## `KUC-168`
**Source**: `notebooks/products/equity/EQUITY_AMERICANOPTION_ComparisonWithQLExample.ipynb`

Validating American option pricing against QuantLib reference implementation.

## `KUC-169`
**Source**: `notebooks/products/equity/EQUITY_ASIAN_OPTIONS.ipynb`

Pricing Asian (average rate) options using geometric and arithmetic averaging methods.

## `KUC-170`
**Source**: `notebooks/products/equity/EQUITY_BARRIER_OPTIONS.ipynb`

Pricing barrier options (up-and-out, down-and-in, etc.) with Greeks calculation.

## `KUC-171`
**Source**: `notebooks/products/equity/EQUITY_BASKET_OPTIONS.ipynb`

Pricing basket options on multiple underlying assets using moment matching.

## `KUC-172`
**Source**: `notebooks/products/equity/EQUITY_CHOOSER_OPTION.ipynb`

Pricing chooser options that allow selection of call or put at a future date.

## `KUC-173`
**Source**: `notebooks/products/equity/EQUITY_CLIQUET_OPTION.ipynb`

Pricing cliquet (reset) options with periodic coupon-like payoffs based on performance.

## `KUC-174`
**Source**: `notebooks/products/equity/EQUITY_COMPOUND_OPTION_CompareWithML.ipynb`

Pricing compound options (option on option) and comparing with machine learning approaches.

## `KUC-175`
**Source**: `notebooks/products/equity/EQUITY_DIGITALOPTION_BasicValuation.ipynb`

Pricing digital options with asset-or-nothing payoff and calculating Greeks.

## `KUC-176`
**Source**: `notebooks/products/equity/EQUITY_DIGITAL_CASH_OR_NOTHING_OPTION.ipynb`

Pricing cash-or-nothing digital options with fixed payoff upon condition.

## `KUC-177`
**Source**: `notebooks/products/equity/EQUITY_FIXED_LOOKBACK_OPTION.ipynb`

Pricing fixed strike lookback options using Monte Carlo simulation.

## `KUC-178`
**Source**: `notebooks/products/equity/EQUITY_FLOAT_LOOKBACK_OPTION.ipynb`

Pricing floating strike lookback options where strike is determined by extreme price.

## `KUC-179`
**Source**: `notebooks/products/equity/EQUITY_ONE_TOUCH_OPTION.ipynb`

Pricing one-touch (digital) options that pay upon touching a barrier level.

## `KUC-180`
**Source**: `notebooks/products/equity/EQUITY_RAINBOW_OPTION.ipynb`

Pricing rainbow options on multiple assets with various payoff structures.

## `KUC-181`
**Source**: `notebooks/products/equity/EQUITY_VANILLA_AMERICAN_STYLE_OPTION.ipynb`

Pricing American vanilla options using LSMC and finite difference methods.

## `KUC-182`
**Source**: `notebooks/products/equity/EQUITY_VANILLA_EUROPEAN_STYLE_MONTE_CARLO_SOBOL.ipynb`

European option pricing using Sobol quasi-random sequences for Monte Carlo.

## `KUC-183`
**Source**: `notebooks/products/equity/EQUITY_VANILLA_EUROPEAN_STYLE_MONTE_CARLO_TIMINGS.ipynb`

Performance benchmarking of Monte Carlo implementations with different libraries.

## `KUC-184`
**Source**: `notebooks/products/equity/EQUITY_VANILLA_EUROPEAN_STYLE_OPTION HIGH VOL LIMIT.ipynb`

Analyzing European option behavior in high volatility limiting cases.

## `KUC-185`
**Source**: `notebooks/products/equity/EQUITY_VANILLA_EUROPEAN_STYLE_OPTION.ipynb`

European option pricing with full Greeks calculation (delta, gamma, theta, vega, rho).

## `KUC-186`
**Source**: `notebooks/products/equity/EQUITY_VANILLA_EUROPEAN_STYLE_OPTION_VECTORISATION.ipynb`

Vectorized European option pricing for multiple strikes, expiries, or option types simultaneously.

## `KUC-187`
**Source**: `notebooks/products/equity/EQUITY_VANILLA_OPTION_IntradayValuationAndGreeks.ipynb`

Intraday option pricing with hourly Greeks updates for trading desks.

## `KUC-188`
**Source**: `notebooks/products/equity/EQUITY_VARIANCESWAP_Basic_Example.ipynb`

Pricing variance swaps and calculating fair strike using realized volatility from option surface.
