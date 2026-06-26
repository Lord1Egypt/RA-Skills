# Known Use Cases (KUC)

Total: **5**

## `KUC-101`
**Source**: `fava_investor/cli/investor.py`

Provides a unified command-line interface for portfolio management operations including tax loss harvesting, asset allocation analysis, cash drag detection, and tax gain minimization.

## `KUC-102`
**Source**: `fava_investor/util/test_relatetickers.py`

Identifies and groups equivalent or substitutable securities (e.g., VTI, VTSAX, VTSMX) based on metadata annotations to support tax lot management and wash sale detection.

## `KUC-103`
**Source**: `fava_investor/modules/minimizegains/test_minimizegains.py`

Determines optimal sell order for securities to minimize realized capital gains by analyzing cost basis and holding periods across multiple lots.

## `KUC-104`
**Source**: `fava_investor/modules/assetalloc_class/test_asset_allocation.py`

Calculates and reports portfolio allocation breakdown by asset type (stocks, bonds, cash, etc.) with percentage distributions from investment account holdings.

## `KUC-105`
**Source**: `fava_investor/modules/tlh/test_libtlh.py`

Identifies securities with unrealized losses that can be sold to harvest tax losses, typically looking back 30 days to find positions eligible for wash sale rule exceptions.
