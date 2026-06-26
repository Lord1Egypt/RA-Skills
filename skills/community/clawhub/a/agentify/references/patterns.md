# Transformation Patterns

Before/after examples for agent-friendly transformations.

## Table of Contents
- [1. Nav: div → semantic](#1-nav-div--semantic)
- [2. Layout: div → landmarks](#2-layout-div--landmarks)
- [3. Icon button: add label](#3-icon-button-add-label)
- [4. Input: placeholder-only → labeled](#4-input-placeholder-only--labeled)
- [5. Form: ungrouped → fieldset](#5-form-ungrouped--fieldset)
- [6. Product card: add structured data](#6-product-card-add-structured-data)
- [7. Article: add metadata](#7-article-add-metadata)
- [8. Accordion: add state](#8-accordion-add-state)
- [9. Tabs: add ARIA](#9-tabs-add-aria)
- [10. Image: add alt](#10-image-add-alt)
- [11. Table: add headers](#11-table-add-headers)
- [12. Links: generic → descriptive](#12-links-generic--descriptive)
- [13. Modal: add dialog semantics](#13-modal-add-dialog-semantics)

---

## 1. Nav: div → semantic

Before:
```html
<div class="nav-bar">
  <div class="nav-item"><a href="/">Home</a></div>
  <div class="nav-item active"><a href="/products">Products</a></div>
</div>
```

After:
```html
<nav aria-label="Main navigation" data-testid="main-nav">
  <ul>
    <li><a href="/" data-testid="nav-home">Home</a></li>
    <li><a href="/products" aria-current="page" data-testid="nav-products">Products</a></li>
  </ul>
</nav>
```

---

## 2. Layout: div → landmarks

Before:
```html
<div class="page">
  <div class="top-bar">...</div>
  <div class="content">...</div>
  <div class="sidebar">...</div>
  <div class="bottom">...</div>
</div>
```

After:
```html
<div class="page">
  <header class="top-bar" data-testid="page-header">...</header>
  <main class="content" id="main-content" data-testid="page-main">...</main>
  <aside class="sidebar" data-testid="page-sidebar">...</aside>
  <footer class="bottom" data-testid="page-footer">...</footer>
</div>
```

---

## 3. Icon button: add label

Before:
```html
<button class="btn-close" onclick="closeModal()">
  <svg><!-- X icon --></svg>
</button>
```

After:
```html
<button class="btn-close" onclick="closeModal()" aria-label="Close dialog" data-testid="close-modal-btn">
  <svg aria-hidden="true"><!-- X icon --></svg>
</button>
```

---

## 4. Input: placeholder-only → labeled

Before:
```html
<input type="text" placeholder="Enter your email" class="email-input">
```

After:
```html
<label for="user-email">Email address</label>
<input id="user-email" type="email" name="email" placeholder="Enter your email"
       class="email-input" autocomplete="email" data-testid="email-input">
```

---

## 5. Form: ungrouped → fieldset

Before:
```html
<form>
  <input type="text" placeholder="First name">
  <input type="text" placeholder="Last name">
  <input type="text" placeholder="Street">
  <input type="text" placeholder="City">
  <button type="submit">Save</button>
</form>
```

After:
```html
<form data-testid="address-form">
  <fieldset>
    <legend>Personal Information</legend>
    <label for="first-name">First name</label>
    <input id="first-name" type="text" name="firstName" autocomplete="given-name" data-testid="first-name-input">
    <label for="last-name">Last name</label>
    <input id="last-name" type="text" name="lastName" autocomplete="family-name" data-testid="last-name-input">
  </fieldset>
  <fieldset>
    <legend>Address</legend>
    <label for="street">Street</label>
    <input id="street" type="text" name="street" autocomplete="street-address" data-testid="street-input">
    <label for="city">City</label>
    <input id="city" type="text" name="city" autocomplete="address-level2" data-testid="city-input">
  </fieldset>
  <button type="submit" data-testid="save-btn">Save</button>
</form>
```

---

## 6. Product card: add structured data

Before:
```html
<div class="product-card">
  <img src="/img/shoes.jpg">
  <div class="title">Running Shoes</div>
  <div class="price">$89.99</div>
  <button>Add to Cart</button>
</div>
```

After:
```html
<article class="product-card" data-testid="product-card" data-entity-type="product">
  <img src="/img/shoes.jpg" alt="Running Shoes" data-testid="product-image">
  <h3 class="title" data-testid="product-title">Running Shoes</h3>
  <p class="price" data-testid="product-price"><data value="89.99">$89.99</data></p>
  <button data-testid="add-to-cart-btn" data-action="add-to-cart">Add to Cart</button>
</article>
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "Running Shoes",
  "image": "/img/shoes.jpg",
  "offers": { "@type": "Offer", "price": "89.99", "priceCurrency": "USD" }
}
</script>
```

---

## 7. Article: add metadata

Before:
```html
<div class="post">
  <div class="post-title">Understanding WebAssembly</div>
  <div class="post-meta">By John Doe · January 15, 2025</div>
  <div class="post-body"><p>WebAssembly is...</p></div>
</div>
```

After:
```html
<article class="post" data-testid="blog-post" data-entity-type="article">
  <h2 class="post-title" data-testid="post-title">Understanding WebAssembly</h2>
  <p class="post-meta">By <span data-testid="post-author">John Doe</span> ·
    <time datetime="2025-01-15" data-testid="post-date">January 15, 2025</time></p>
  <div class="post-body" data-testid="post-body"><p>WebAssembly is...</p></div>
</article>
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "BlogPosting",
  "headline": "Understanding WebAssembly",
  "author": { "@type": "Person", "name": "John Doe" },
  "datePublished": "2025-01-15"
}
</script>
```

---

## 8. Accordion: add state

Before:
```html
<div class="faq-item">
  <div class="faq-question" onclick="toggle(this)">What is your return policy?</div>
  <div class="faq-answer" style="display:none">You can return items within 30 days.</div>
</div>
```

After:
```html
<div class="faq-item" data-testid="faq-item">
  <button class="faq-question" onclick="toggle(this)" aria-expanded="false"
          aria-controls="faq-answer-1" data-testid="faq-question">
    What is your return policy?
  </button>
  <div class="faq-answer" id="faq-answer-1" role="region" style="display:none" data-testid="faq-answer">
    <p>You can return items within 30 days.</p>
  </div>
</div>
```

---

## 9. Tabs: add ARIA

Before:
```html
<div class="tabs">
  <div class="tab active" onclick="showTab(0)">Overview</div>
  <div class="tab" onclick="showTab(1)">Specs</div>
</div>
<div class="tab-content" id="tab-0">Overview content...</div>
```

After:
```html
<div class="tabs" role="tablist" aria-label="Product information" data-testid="product-tabs">
  <button class="tab active" role="tab" onclick="showTab(0)" aria-selected="true"
          aria-controls="tab-panel-0" id="tab-0" data-testid="tab-overview">Overview</button>
  <button class="tab" role="tab" onclick="showTab(1)" aria-selected="false"
          aria-controls="tab-panel-1" id="tab-1" data-testid="tab-specs">Specs</button>
</div>
<div class="tab-content" id="tab-panel-0" role="tabpanel" aria-labelledby="tab-0"
     data-testid="tabpanel-overview">Overview content...</div>
```

---

## 10. Image: add alt

Before:
```html
<img src="/hero.jpg" class="hero-image">
<img src="/decorative-line.svg" class="divider">
```

After:
```html
<img src="/hero.jpg" class="hero-image" alt="Product showcase: wireless headphones" data-testid="hero-image">
<img src="/decorative-line.svg" class="divider" alt="" aria-hidden="true">
```

---

## 11. Table: add headers

Before:
```html
<table>
  <tr><td>Name</td><td>Price</td><td>Stock</td></tr>
  <tr><td>Widget A</td><td>$10</td><td>In stock</td></tr>
</table>
```

After:
```html
<table data-testid="products-table">
  <thead>
    <tr><th scope="col">Name</th><th scope="col">Price</th><th scope="col">Stock</th></tr>
  </thead>
  <tbody>
    <tr data-entity-type="product" data-entity-id="widget-a">
      <td data-testid="product-name">Widget A</td>
      <td data-testid="product-price"><data value="10">$10</data></td>
      <td data-testid="product-stock" data-state="in-stock">In stock</td>
    </tr>
  </tbody>
</table>
```

---

## 12. Links: generic → descriptive

Before:
```html
<p>To view pricing, <a href="/pricing">click here</a>.</p>
```

After:
```html
<p><a href="/pricing" data-testid="pricing-link">View our pricing</a>.</p>
```

---

## 13. Modal: add dialog semantics

Before:
```html
<div class="modal">
  <div class="modal-header">Confirm Delete</div>
  <button onclick="confirm()">Yes</button>
  <button onclick="cancel()">No</button>
</div>
```

After:
```html
<div class="modal" role="dialog" aria-modal="true" aria-labelledby="modal-title"
     data-testid="confirm-delete-dialog">
  <h2 id="modal-title" data-testid="modal-title">Confirm Delete</h2>
  <button onclick="confirm()" data-testid="confirm-btn" data-action="confirm-delete">Yes, delete</button>
  <button onclick="cancel()" data-testid="cancel-btn" data-action="cancel">No, cancel</button>
</div>
```
