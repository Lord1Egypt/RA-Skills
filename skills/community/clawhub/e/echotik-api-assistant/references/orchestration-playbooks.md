# Business Orchestration Playbooks

Use these playbooks when the user asks for a report, a workflow recommendation, a multi-step analysis, or a business-facing answer rather than a single raw endpoint call.

## 1. Creator Health Report

### Recommended Core Sections

- creator detail
- recent or historical trend
- recent videos
- live history
- promoted products

### Extended Sections

- follower list
- following list
- region
- milestones

### Recommended Workflow

1. `Influencer Detail - EchoTik` or `Influencer Detail - Realtime`
2. `Influencer Trend - EchoTik`
3. `Influencer Video List - EchoTik` or realtime creator video list
4. `Influencer Live List - EchoTik`
5. `Influencer Product List - EchoTik`
6. optional: follower list, following list, region, milestones

### When To Prefer Realtime

- the user wants the latest public profile state
- the user wants follower/following data
- the user wants region or milestone data

## 2. Creator Discovery Shortlist

### Recommended Workflow

1. `Influencer Rank List - EchoTik` for leaderboard-style requests
2. `Influencer List - EchoTik` for high-dimensional filtering
3. optional: `Influencer Detail - EchoTik` for shortlisted enrichment

### Best For

- fastest follower growth
- top commerce creators
- category-filtered creator sourcing

## 3. Product Opportunity Report

### Recommended Core Sections

- product detail
- product trend
- related creators
- related videos
- related live sessions

### Extended Sections

- comments
- leaderboard context

### Recommended Workflow

1. resolve `product_id` from a share link if needed
2. `Product Detail - EchoTik` or realtime product detail
3. `Product Trend - EchoTik`
4. `Product Influencer List - EchoTik`
5. `Product Video List - EchoTik`
6. `Product Live List - EchoTik`
7. optional: product comments
8. optional: `Product Rank List - EchoTik`

### When To Prefer Realtime

- offline detail is empty
- the user wants fresher comments

## 4. Product Discovery Workflow

### Recommended Workflow

1. resolve category IDs if the request is category-driven
2. `Product List - EchoTik`
3. optional: `Product Rank List - EchoTik`
4. optional: enrich shortlisted products through detail

### Best For

- winning product discovery
- category sourcing
- GMV- or sales-filtered product screens

## 5. Seller Performance Report

### Recommended Core Sections

- seller detail
- seller trend
- product inventory
- related creators
- related videos
- related live sessions

### Extended Sections

- leaderboard context

### Recommended Workflow

1. `Seller Detail - EchoTik`
2. `Seller Trend - EchoTik`
3. `Seller Product List - EchoTik` or realtime seller product list
4. `Seller Influencer List - EchoTik`
5. `Seller Video List - EchoTik`
6. `Seller Live List - EchoTik`
7. optional: `Seller Rank List - EchoTik`

### When To Prefer Realtime

- the user wants the current shop inventory instead of the collected offline inventory

## 6. Seller Discovery Workflow

### Recommended Workflow

1. resolve seller-category IDs if the request is category-driven
2. `Seller List - EchoTik`
3. optional: `Seller Rank List - EchoTik`
4. optional: enrich shortlisted sellers through detail

### Best For

- cross-border versus local shop discovery
- live-led versus video-led seller discovery
- category-filtered seller sourcing

## 7. Video Performance Analysis

### Recommended Workflow

1. realtime or offline video detail, depending on the user's choice
2. `Video 14-Day Interaction Trend - Realtime`
3. `Video Comment Keyword Insight - Realtime`
4. optional: raw video comments
5. optional: comment replies
6. optional: video captions
7. optional: linked products

### Best For

- why this video performed well
- recent interaction acceleration
- comment theme analysis
- caption or scripting analysis

## 8. Video Discovery Workflow

### Recommended Workflow

1. resolve product category IDs if needed
2. `Video List - EchoTik`
3. optional: `Video Rank List - EchoTik`
4. optional: `Video Detail - EchoTik` or realtime detail for shortlisted videos

### Best For

- commerce-video mining
- AI-video screening
- ad-video screening

## 9. Search Workflow

### Priority Order

1. dedicated realtime search endpoint for the target entity
2. universal EchoTik search as fallback
3. detail enrichment after search if richer fields are needed

### Entity Mapping

- creators: realtime creator search
- products: realtime product search
- videos: realtime video search
- live sessions: realtime live search
- hashtags: realtime hashtag search
- music: realtime music search

## 10. Image-Based Product Search Workflow

### Recommended Workflow

1. `Product Photo Search - Realtime`
2. capture `image_uri` and `box_detection`
3. `Product Photo Search Page - Realtime` for additional results
4. optional: product detail for shortlisted results

## 11. Hashtag Video Exploration

### Recommended Workflow

1. realtime hashtag search if only text is known
2. hashtag video list through `hashtag_id`
3. optional: realtime or offline video detail for shortlisted videos

## 12. Live Room Monitoring

### Recommended Workflow

1. realtime live detail

### Constraint

- this only works when the room is currently live
