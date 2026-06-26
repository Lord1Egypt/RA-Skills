# Website Behavioral Analytics

## GTM Architecture: Tags, Triggers, Variables

```
Tag      = What to do   (send event to GA4, fire pixel, etc.)
Trigger  = When to do it (on scroll, on click, on form submit)
Variable = What to include (element text, page URL, user ID, etc.)
```

**Standard GTM setup flow:**
1. Install GTM snippet (`<head>` + `<body>`)
2. Create Google Tag (replaces old GA4 Configuration Tag — 2025 standard)
3. Add Data Layer variables for custom dimensions
4. Create triggers for each user interaction
5. Create GA4 Event tags linked to triggers
6. Test in Preview/Tag Assistant mode
7. Debug in GA4 DebugView (Admin → DebugView)
8. Publish when clean

---

## Session-Level Tracking

### What to Collect
```javascript
// Push on every page load
dataLayer.push({
  event: 'session_started',
  session_id: generateSessionId(),           // UUID, persist in sessionStorage
  user_id: getUserHash(),                    // hashed, from auth system
  timestamp: new Date().toISOString(),
  traffic_source: document.referrer || 'direct',
  utm_source: getParam('utm_source'),
  utm_medium: getParam('utm_medium'),
  utm_campaign: getParam('utm_campaign'),
  landing_page: window.location.pathname,
  device_type: getDeviceType(),              // mobile/tablet/desktop
  browser: navigator.userAgent,
  os: getOS(),
});
```

### Bounce & Exit Tracking
```javascript
// Track exit page
window.addEventListener('beforeunload', () => {
  dataLayer.push({
    event: 'session_ended',
    exit_page: window.location.pathname,
    session_duration: Math.round((Date.now() - sessionStart) / 1000),
    pages_viewed: pageCount,
  });
});
```

---

## Scroll Depth Tracking

**GA4 default:** Only fires at 90%. Always supplement with GTM custom scroll tracking.

### GTM Setup (25/50/75/100% thresholds)
1. In GTM → Triggers → New → Scroll Depth
2. Enable: Vertical Scroll Depths
3. Set percentages: `25, 50, 75, 100`
4. Trigger on: All Pages (or specific page types)

**GA4 Event Tag:**
```
Event name: scroll_depth
Parameters:
  percent_scrolled: {{Scroll Depth Threshold}}
  page_path: {{Page Path}}
  content_type: {{content_type variable}}   // blog/product/landing/etc.
```

**Analysis tip:** Cross-reference scroll depth with session duration.
Fast scroll to 100% = skimmer. Slow scroll to 75% = engaged reader.
Don't compare blog posts to product pages — normalize by content type.

### Common Patterns by Page Type
| Page Type | Healthy 75%+ Rate | Action if Low |
|---|---|---|
| Blog post | 40–60% | Add more visuals, break up text |
| Landing page | 30–50% | Move CTA higher; hero may be converting early |
| Product page | 35–55% | Check if key info (price, specs) is below fold |
| Checkout | >70% | Critical — any low scroll is a funnel problem |

---

## Form Abandonment Tracking

### GTM Implementation (Data Layer Listener)
```javascript
// Paste as Custom HTML tag, fire on: Pages containing the form
(function() {
  if (typeof document.querySelectorAll === "undefined") return;
  var history = {};

  document.addEventListener("change", function(e) {
    var target = e.target;
    var tags = ["INPUT", "TEXTAREA", "SELECT"];
    if (target && target.tagName && tags.includes(target.tagName.toUpperCase())) {
      var fieldName = target.getAttribute("name") || target.getAttribute("id") || target.tagName;
      var formId = target.form ? (target.form.id || "unknown_form") : "unknown_form";
      if (!history[formId]) history[formId] = [];
      if (history[formId].slice(-1)[0] !== fieldName) {
        history[formId].push(fieldName);
      }
    }
  });

  window.addEventListener("beforeunload", function() {
    Object.keys(history).forEach(function(formId) {
      // Only fire if form was NOT submitted
      var submitted = window._submittedForms && window._submittedForms[formId];
      if (!submitted && history[formId].length > 0) {
        dataLayer.push({
          event: 'form_abandoned',
          form_id: formId,
          last_field_touched: history[formId].slice(-1)[0],
          fields_touched: history[formId].join(' > '),
          fields_count: history[formId].length,
        });
      }
    });
  });

  // Mark form as submitted on success
  document.addEventListener("submit", function(e) {
    var formId = e.target.id || "unknown_form";
    window._submittedForms = window._submittedForms || {};
    window._submittedForms[formId] = true;
    dataLayer.push({
      event: 'form_submitted',
      form_id: formId,
    });
  });
})();
```

**Limitations:** Doesn't work in Safari or IE. AJAX forms require custom event on successful XHR.

### GA4 Event Parameters to Send
```
form_abandoned:
  form_id, form_name, last_field_touched, fields_touched, page_path

form_submitted:
  form_id, form_name, page_path
```

**Key Metric:** Abandonment rate by field = which field causes most drop-offs.
If 60% of abandoners stop at "Phone Number" field — make it optional.

---

## Page Path & Feature Usage Tracking

### Button / CTA Click Tracking
**GTM Trigger:** Click - All Elements, with filters:
- Click ID contains `cta` OR Click Classes contains `btn-primary`

Or use specific element selectors for important CTAs.

```javascript
// Preferred: push from the app directly
dataLayer.push({
  event: 'button_clicked',
  element_id: 'hero_cta',
  element_text: 'Start Free Trial',
  element_location: 'hero_section',
  page_path: window.location.pathname,
});
```

### Internal Site Search
```javascript
// Fire on search results page load
dataLayer.push({
  event: 'site_search',
  search_query: getParam('q') || getParam('search'),
  results_count: document.querySelectorAll('.search-result').length,
});
```

### Video Engagement (YouTube via GTM)
GTM has a built-in **YouTube Video Trigger** (Enhanced Measurement in GA4 handles basic cases).
Custom events to supplement:
```
video_started:    video_title, video_id, video_percent: 0
video_progress:   video_percent: 25 / 50 / 75
video_completed:  video_percent: 100, video_duration
```

### Product Page Tracking (E-commerce)
```javascript
dataLayer.push({
  event: 'product_viewed',
  item_id: 'SKU123',
  item_name: 'Blue T-Shirt',
  item_category: 'Apparel',
  price: 29.99,
  currency: 'USD',
  time_on_page: timeOnPage,         // seconds
});
```

---

## User-Level Data Collection

### What to Track Per User (in GA4 User Properties or CDP)
```
first_visit_date      last_visit_date       visit_count
total_sessions        total_pages_viewed    avg_session_duration
primary_source        conversion_status     conversion_date
customer_ltv          engagement_score      cohort_month
preferred_device      feature_usage_score
```

### Cohort Tracking
Tag users with their acquisition source + date at first visit.
Store in GA4 User Properties:
```javascript
gtag('set', 'user_properties', {
  acquisition_month: '2025-03',
  acquisition_source: 'google_cpc',
  user_type: 'returning',          // new / returning / churned
});
```

---

## GA4 Debug & Quality Assurance

### Testing Flow
1. Enable GTM Preview Mode
2. Navigate to your site — GTM Assistant shows all fired tags
3. Open GA4 → Admin → DebugView → see events in real time
4. Check: correct event names, correct parameters, no duplicates
5. Verify `user_id` is consistent across pages
6. Submit GTM version only when everything passes

### Common Issues & Fixes
| Problem | Cause | Fix |
|---|---|---|
| Events firing twice | Duplicate tag or trigger | Check trigger conditions; use "Once per page" |
| Scroll events not firing | JS error before GTM loads | Move GTM snippet higher in `<head>` |
| Form abandoned fires on submit | Missing submitted-form flag | Add submit listener to exclude submitted forms |
| user_id undefined | Auth state not ready at page load | Delay dataLayer push until auth resolves |
| GA4 shows null parameters | Custom dimension not registered | Register in GA4 → Admin → Custom Definitions |
| SPA page changes not tracked | No history change trigger | Add History Change trigger in GTM |

---

## Real-Time Collection Architecture

For true real-time event streaming (not GA4's 30-second batching):

```
User action
  → dataLayer.push()
  → GTM fires tag
  → GA4 Measurement Protocol (server-side, real-time)
  → BigQuery streaming insert

OR:

User action
  → Custom JavaScript fetch()
  → Your server endpoint
  → Kafka / Pub-Sub event stream
  → BigQuery / Clickhouse / Snowflake
```

GA4 has a built-in BigQuery export (daily by default; streaming available on paid plans).
For true real-time, use Measurement Protocol + server-side event streaming.
