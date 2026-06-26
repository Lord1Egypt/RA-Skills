---
title: Competitive Analysis Data Contract
source: .docs/竞品分析/竞品分析建表.sql
---

# Competitive Analysis Data Contract

This file defines the data contract, field usage, and trigger-table expectations used by the CLI.

## Existing Tables

### `competitive_product_list`

Purpose:

- stores the product list to analyze
- provides the main `category` aggregation key
- acts as the parent table for reviews and QA

Key fields:

- `category`
- `product_id`
- `shop_name`
- `product_url`
- `product_name`
- `etl_date`
- `etl_time`

### `competitive_review`

Purpose:

- stores product reviews
- used to extract needs, pain points, sentiment, and feature keywords

Key fields:

- `product_id`
- `review_time`
- `review_content`
- `etl_date`
- `etl_time`

### `competitive_qa`

Purpose:

- stores product QA
- used to extract purchase concerns and pre-sale questions

Key fields:

- `product_id`
- `question`
- `answer`
- `etl_date`
- `etl_time`

### `competitive_crawl_trigger`

Purpose:

- records crawl completion events
- acts as the trigger source for the downstream CLI

Existing key fields:

- `update_time`
- `task_type`
- `status`
- `etl_date`
- `etl_time`

## Required Trigger Fields

This skill assumes these fields already exist on `competitive_crawl_trigger`. The skill package does not create or alter tables.

Required fields:

- `is_consumed BOOLEAN NOT NULL DEFAULT FALSE`
- `consumed_at TIMESTAMP NULL`
- `consume_status VARCHAR(20) NOT NULL DEFAULT 'pending'`
- `consume_attempts INTEGER NOT NULL DEFAULT 0`
- `consume_error TEXT NULL`
- `last_report_path TEXT NULL`

Why they exist:

- `is_consumed`: prevents duplicate processing
- `consumed_at`: records when consumption finished
- `consume_status`: tracks `pending/success/failed`
- `consume_attempts`: tracks retry attempts
- `consume_error`: stores the latest failure reason
- `last_report_path`: stores the latest report locator, typically the OSS manifest URL

## Query Rules

### Time Window

- default analysis window is the last 6 months
- product-level filtering uses `competitive_product_list.etl_date`
- review-level filtering prefers `review_time`, then falls back to `etl_time`
- QA-level filtering uses `etl_time`

### Aggregation Dimensions

- primary dimension: `category`
- secondary dimensions: brand, shop, feature terms, need terms, pain terms, QA intent categories

### Joins

- `competitive_review.product_id = competitive_product_list.product_id`
- `competitive_qa.product_id = competitive_product_list.product_id`

## Current Gaps

The following metrics from the reference PDF cannot be reliably computed from the current schema alone:

- sales revenue
- price
- explicit brand field
- target age
- explicit product positioning

Handling rules:

1. Keep the report structure unchanged.
2. Use explainable heuristics when inference is possible.
3. Use `未采集` or `待补充` when inference is not possible.
4. Never fabricate precise values.

## Heuristic Rules

### Brand

- prefer `shop_name`
- strip suffixes such as `旗舰店`, `专营店`, and `官方店`
- if missing, fall back to the leading part of `product_name`

### Core Features And Tags

- match keywords from `product_name`, reviews, and QA text
- current default dictionaries include:
  - feature terms: `护脊`, `分区`, `可水洗`, `四季通用`, `记忆棉`
  - material terms: `硅胶`, `纱布`, `蚕丝`, `乳胶`
  - visual or emotion terms: `云朵`, `IP`, `卡通`

### Needs And Pain Points

- count them using review keyword dictionaries
- feed the top needs and pain points into Section 5

### Purchase Barriers

- match intent keywords from QA `question`
- examples: quality, age, softness, height, cleaning, breathability, smell

## Pre-run Validation

The CLI should validate:

1. `competitive_crawl_trigger` contains all required consumption fields
2. there are unconsumed rows with `status='success'`
3. at least one `category` has product data inside the analysis window

If the consumption fields are missing, fail fast and ask the operator to fix the database schema first.
