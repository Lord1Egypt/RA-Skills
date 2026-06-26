# Known Use Cases (KUC)

Total: **40**

## `KUC-001`
**Source**: `docs/source/deal_sample/test01.py`

Model a basic asset-backed securities deal with mortgage pool, bonds, fees, and waterfall to analyze cashflows and tranche performance

## `KUC-002`
**Source**: `docs/source/deal_sample/arm_sample.py`

Model an adjustable rate mortgage pool with LIBOR-based floating rates and periodic resets

## `KUC-003`
**Source**: `docs/source/deal_sample/bondStepUp.py`

Model bonds with scheduled rate step-ups at specific dates for ABS deal structuring

## `KUC-004`
**Source**: `docs/source/deal_sample/test10.py`

Incorporate interest rate swap to hedge floating rate exposure in ABS deal

## `KUC-005`
**Source**: `docs/source/deal_sample/conditionAgg.py`

Implement conditional aggregation rules in waterfall that trigger based on pool status

## `KUC-006`
**Source**: `docs/source/deal_sample/fee1.py`

Calculate fees based on period, pool balance percentages, and tiered tables in ABS deals

## `KUC-007`
**Source**: `docs/source/deal_sample/fireTrigger.py`

Implement trigger mechanisms that fire events in waterfall based on performance conditions

## `KUC-008`
**Source**: `docs/source/deal_sample/float_bond.py`

Model ABS deal with floating rate bonds tied to SOFR index

## `KUC-009`
**Source**: `docs/source/deal_sample/multi_pool.py`

Model ABS deal with multiple pools containing different asset types (mortgage and loan) with separate assumptions

## `KUC-010`
**Source**: `docs/source/deal_sample/payPrinSeq.py`

Structure sequential principal payments across multiple bond tranches

## `KUC-011`
**Source**: `docs/source/deal_sample/rateCap.py`

Implement interest rate cap to limit floating rate exposure in ABS deal

## `KUC-012`
**Source**: `docs/source/deal_sample/resec.py`

Model re-securitization where bonds from underlying deals become assets in a new structure

## `KUC-013`
**Source**: `docs/source/deal_sample/stepup_sample.py`

Model bonds with conditional step-up rates that increase after specified dates

## `KUC-014`
**Source**: `docs/source/deal_sample/test02.py`

Implement multiple waterfall phases (amortizing, accelerated) with different payment priorities

## `KUC-015`
**Source**: `docs/source/deal_sample/test04.py`

Split pool income (interest/principal) proportionally across multiple accounts

## `KUC-016`
**Source**: `docs/source/deal_sample/test05.py`

Model insurance or liquidation provider supporting interest payments when pool income is insufficient

## `KUC-017`
**Source**: `docs/source/deal_sample/test08.py`

Model GNMA (Ginnie Mae) mortgage-backed deal with custom ARM loans, guarantor fees, and servicer fees

## `KUC-018`
**Source**: `docs/source/deal_sample/ysoc.py`

Implement yield supplement overcollateralization to bridge yield gap between low-rate assets and higher-rate bonds

## `KUC-019`
**Source**: `docs/source/deal_sample/test13.py`

Model assets with pre-defined projected cashflows rather than individual loan calculations

## `KUC-020`
**Source**: `docs/source/nbsample/pool_multiScenario.ipynb`

Run single pool through multiple CDR/CPR scenarios to compare default and prepayment impacts

## `KUC-021`
**Source**: `docs/source/nbsample/multiAsset.ipynb`

Run multiple asset pools (Mortgage, Loan) with separate assumptions and inspect pool balances

## `KUC-022`
**Source**: `docs/source/nbsample/single_mortgage.ipynb`

Project cashflows for individual mortgage with various CDR scenarios

## `KUC-023`
**Source**: `docs/source/nbsample/single_loan.ipynb`

Model individual loan with SOFR-based floating rate and rate assumption scenarios

## `KUC-024`
**Source**: `docs/source/nbsample/How-to-price-Balloon-Mortgage.ipynb`

Price balloon mortgages and analyze impact of default assumptions on pricing

## `KUC-025`
**Source**: `docs/source/nbsample/bond_pricing.ipynb`

Price bonds using discount curve to determine present value of cashflows

## `KUC-026`
**Source**: `docs/source/nbsample/firstLoss.ipynb`

Calculate first loss position and equity tranche absorption using root finder

## `KUC-027`
**Source**: `docs/source/nbsample/triggers.ipynb`

Monitor default rate triggers and cumulative defaults over deal life

## `KUC-028`
**Source**: `docs/source/nbsample/HowDealEnded.ipynb`

Model deal call options and determine deal termination conditions

## `KUC-029`
**Source**: `docs/source/nbsample/Irr_002.ipynb`

Calculate IRR for equity tranche with target return and incentive fee structure

## `KUC-030`
**Source**: `docs/source/nbsample/masterTrust.ipynb`

Model master trust with multiple sub-tranches (A-1, A-2) under same series

## `KUC-031`
**Source**: `docs/source/nbsample/comboSensitivity.ipynb`

Run combined scenarios with different deal structures and pool assumptions

## `KUC-032`
**Source**: `docs/source/nbsample/InspectSample.ipynb`

Inspect and extract intermediate waterfall variables for debugging deal logic

## `KUC-033`
**Source**: `docs/source/nbsample/re_securitization_example.ipynb`

Model complete re-securitization with child deals, parent deal, and asset pooling from bond proceeds

## `KUC-034`
**Source**: `docs/source/nbsample/revolving_buy_multiple_pools.ipynb`

Model revolving credit structure that purchases multiple pools of assets over time

## `KUC-035`
**Source**: `docs/source/nbsample/warehouse.ipynb`

Model warehouse facility with funding period before term deal issuance

## `KUC-036`
**Source**: `docs/source/nbsample/SRT_Example_Native_Prod.ipynb`

Model synthetic risk transfer where credit risk is transferred via derivatives rather than asset transfer

## `KUC-037`
**Source**: `docs/source/nbsample/PoolAndTag.ipynb`

Run pool analysis with tag-based filtering and multiple assumption scenarios

## `KUC-038`
**Source**: `docs/source/nbsample/MultiIntBond.ipynb`

Model bond with multiple interest components (multipliers and separate rate types)

## `KUC-039`
**Source**: `docs/source/nbsample/structuring-lease-doc.ipynb`

Structure ABS deal backed by lease assets with rental income collections

## `KUC-040`
**Source**: `docs/source/nbsample/WhyByTerm.ipynb`

Apply time-varying assumptions by term periods for CPR and other parameters
