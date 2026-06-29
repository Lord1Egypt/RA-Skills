---
name: Energy-Carbon Management Suite
slug: energy-carbon-management
description: Enterprise-grade energy optimization and carbon accounting skill. Tracks Scope 1/2/3 emissions, generates ESG compliance reports, recommends renewable transition pathways, and models carbon credit trading strategies.
version: 1.0.0
author: ai-gaoqian
tags:
  - energy
  - carbon-accounting
  - esg
  - sustainability
  - renewable-energy
  - carbon-credits
  - net-zero
metadata:
  openclaw:
    requires: openclaw>=1.0.0
---

# Energy-Carbon Management Suite

## Overview
Full-stack energy optimization and carbon management skill for enterprises pursuing net-zero targets. Covers GHG Protocol-compliant carbon accounting (Scope 1/2/3), automated ESG report generation (GRI/SASB/TCFD standards), renewable energy transition modeling with ROI calculations, and carbon credit marketplace intelligence.

## Use Cases
- Calculate corporate carbon footprint across all three scopes
- Generate GRI-compliant annual ESG sustainability reports
- Model rooftop solar / wind PPA financial viability with payback period
- Track carbon credit prices on Verra, Gold Standard, and regional exchanges
- Benchmark energy efficiency against industry peers using public data
- Simulate net-zero pathways with cost projections to 2030/2040/2050

## Execution Flow
1. Accept input: energy bills, fleet data, supply chain invoices, or facility specifications
2. Calculate emission factors using IPCC/EPA/DEFRA databases
3. Classify emissions by scope and category per GHG Protocol
4. Generate compliance-ready reports with audit trails
5. Optionally run optimization scenarios: solar sizing, REC purchasing, electrification ROI

## Output Format
- Carbon footprint dashboard (total tCO2e, by scope breakdown, intensity metrics)
- ESG report (structured per GRI standards with data tables and narrative sections)
- Transition roadmap (technology options, CAPEX/OPEX, emission reduction trajectory)
- Carbon credit market snapshot (registry, project type, price/ton, vintage)

## Standards Compliance
- GHG Protocol Corporate Standard
- GRI Universal Standards 2021
- SASB Materiality Framework
- TCFD Climate Risk Disclosure
- EU CSRD and EU Taxonomy alignment
- ISO 14064 Greenhouse Gas Accounting

## Supported Energy Types
Grid electricity, natural gas, diesel, gasoline, LPG, coal, biomass, solar PV, wind, hydro, geothermal, nuclear, hydrogen

## Carbon Registry Coverage
Verra (VCS), Gold Standard, American Carbon Registry, Climate Action Reserve, EU ETS, China CERE

## Notes
- Emission factor databases from IPCC AR6, EPA eGRID, UK DEFRA, and IEA
- Renewable cost data updated quarterly
- Carbon credit pricing refreshed daily
- Supports multi-facility and multi-region aggregation
