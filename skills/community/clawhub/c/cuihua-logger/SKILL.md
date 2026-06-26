---
name: cuihua-logger
description: |
  📝 AI-powered logging assistant that generates production-ready structured logs.
  Automatically add intelligent logging to your code with proper levels, context, and formatting.
  
  Because good logging saves hours of debugging.

metadata:
  openclaw:
    requires:
      bins:
        - node
      env: []
    primaryEnv: null
  
  version: "1.0.0"
  author: "翠花 (Cuihua) - ClawHub Pioneer"
  license: "MIT"
  tags:
    - logging
    - debugging
    - monitoring
    - observability
    - structured-logging
    - winston
    - pino
    - production-ready
  
  capabilities:
    - Auto-generate structured logs
    - Smart log level selection
    - Context-aware logging
    - Performance logging
    - Error tracking
    - Log coverage analysis
    - Multiple logger support (Winston, Pino, Bunyan)
---

# cuihua-logger - Production-Ready Logging 📝

> **Debug faster with intelligent, structured logging.**

An AI-powered logging assistant that automatically:
- 📝 **Generates** structured logs with proper context
- 🎯 **Selects** appropriate log levels (debug, info, warn, error)
- 📊 **Adds** performance metrics and timing
- 🔍 **Detects** missing logs in critical paths
- ⚡ **Optimizes** log output for production

## 🎯 Why cuihua-logger?

**The problem**:
- ❌ Too many `console.log()` everywhere
- ❌ No structure, hard to search
- ❌ Wrong log levels (everything is "info")
- ❌ Missing context (what user? what request?)
- ❌ Performance overhead in production

**cuihua-logger solves all of this.**

---

## 🚀 Quick Start

### Analyze logging coverage

> "Check logging coverage in src/"

### Add structured logging

> "Add logging to getUserById function"

### Generate performance logs

> "Add performance logging to API endpoints"

---

## 🎨 Features

### 1. Structured Logging ✨

```javascript
// ❌ BEFORE - Unstructured
async function getUserById(id) {
  console.log('Getting user:', id);
  const user = await db.query('SELECT * FROM users WHERE id = $1', [id]);
  console.log('User found:', user);
  return user;
}

// ✅ AFTER - Structured
async function getUserById(id) {
  logger.info('Fetching user', { 
    userId: id,
    operation: 'getUserById'
  });
  
  const startTime = Date.now();
  const user = await db.query('SELECT * FROM users WHERE id = $1', [id]);
  const duration = Date.now() - startTime;
  
  logger.info('User fetched successfully', {
    userId: id,
    operation: 'getUserById',
    duration,
    found: !!user
  });
  
  return user;
}
```

### 2. Smart Log Levels 🎯

```javascript
// Automatic level selection based on context

logger.debug('Cache hit', { key, ttl }); // Development only

logger.info('User logged in', { userId, ip }); // Important events

logger.warn('Rate limit approaching', { 
  userId, 
  current: 95, 
  limit: 100 
}); // Potential issues

logger.error('Payment failed', { 
  orderId, 
  error: error.message,
  stack: error.stack 
}); // Critical errors
```

### 3. Performance Logging ⚡

```javascript
async function fetchData() {
  const timer = logger.startTimer();
  
  const data = await expensiveOperation();
  
  timer.done({ level: 'info', message: 'Operation complete' });
  
  return data;
}

// Output: "Operation complete" duration=1234ms
```

### 4. Request Tracking 🔍

```javascript
app.use((req, res, next) => {
  req.requestId = generateId();
  req.logger = logger.child({ 
    requestId: req.requestId,
    method: req.method,
    path: req.path 
  });
  
  req.logger.info('Request started');
  
  res.on('finish', () => {
    req.logger.info('Request completed', {
      statusCode: res.statusCode,
      duration: Date.now() - req.startTime
    });
  });
  
  next();
});
```

---

## 📋 Usage Examples

### Example 1: Add Logging to Function

**User**: "Add logging to processOrder function"

**Generated**:
```javascript
async function processOrder(orderId, items) {
  logger.info('Processing order', { orderId, itemCount: items.length });
  
  try {
    // Validate
    if (!orderId || !items.length) {
      logger.warn('Invalid order data', { orderId, items });
      throw new ValidationError('Invalid order');
    }
    
    // Create order
    const order = await createOrder(orderId, items);
    logger.info('Order created', { orderId, orderNumber: order.number });
    
    // Process payment
    const payment = await processPayment(order);
    logger.info('Payment processed', { 
      orderId, 
      paymentId: payment.id,
      amount: payment.amount 
    });
    
    return order;
    
  } catch (error) {
    logger.error('Order processing failed', {
      orderId,
      error: error.message,
      stack: error.stack
    });
    throw error;
  }
}
```

### Example 2: API Endpoint Logging

```javascript
app.post('/api/users', async (req, res) => {
  const { logger } = req;
  
  logger.info('Creating user', { email: req.body.email });
  
  try {
    const user = await userService.create(req.body);
    
    logger.info('User created successfully', {
      userId: user.id,
      email: user.email
    });
    
    res.status(201).json(user);
    
  } catch (error) {
    logger.error('User creation failed', {
      email: req.body.email,
      error: error.message
    });
    
    res.status(500).json({ error: 'Failed to create user' });
  }
});
```

---

## ⚙️ Logger Configuration

### Winston

```javascript
import winston from 'winston';

const logger = winston.createLogger({
  level: process.env.LOG_LEVEL || 'info',
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.errors({ stack: true }),
    winston.format.json()
  ),
  transports: [
    new winston.transports.File({ filename: 'error.log', level: 'error' }),
    new winston.transports.File({ filename: 'combined.log' })
  ]
});
```

### Pino (fastest)

```javascript
import pino from 'pino';

const logger = pino({
  level: process.env.LOG_LEVEL || 'info',
  timestamp: pino.stdTimeFunctions.isoTime,
  formatters: {
    level: (label) => ({ level: label })
  }
});
```

---

## 📊 Log Levels

| Level | When to Use | Example |
|-------|------------|---------|
| **debug** | Development debugging | `logger.debug('Cache miss', { key })` |
| **info** | Important events | `logger.info('User logged in', { userId })` |
| **warn** | Potential issues | `logger.warn('Rate limit approaching', { userId })` |
| **error** | Errors that need attention | `logger.error('Payment failed', { orderId })` |

---

## 💰 Pricing

### Free
- ✅ Basic log generation
- ✅ Up to 10 files

### Pro ($8/month)
- ✅ Unlimited files
- ✅ Performance logging
- ✅ Request tracking
- ✅ CI/CD integration

### Enterprise ($59/month)
- ✅ Team policies
- ✅ Log aggregation setup
- ✅ Custom formatters

---

## 📚 Best Practices

1. **Always log errors with context**
2. **Use structured logging (objects, not strings)**
3. **Include request IDs for tracing**
4. **Don't log sensitive data (passwords, tokens)**
5. **Use appropriate log levels**

---

## 📜 License

MIT

---

## 🙏 Acknowledgments

Built with 🌸 by 翠花 (Cuihua)

---

**Made with 🌸 | Cuihua Series | ClawHub Pioneer**
