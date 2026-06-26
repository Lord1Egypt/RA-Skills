/**
 * Stripe Webhook Handler
 */

const express = require('express');
const router = express.Router();
const stripe = require('stripe')(require('../config/config').stripe.secretKey);
const logger = require('../utils/logger');
const config = require('../config/config');
const paymentService = require('../services/payment');
const notificationService = require('../services/notification');

router.post('/', async (req, res) => {
  const sig = req.headers['stripe-signature'];

  let event;

  try {
    // Verify webhook signature
    event = stripe.webhooks.constructEvent(
      req.body,
      sig,
      config.stripe.webhookSecret
    );
  } catch (err) {
    logger.error('Stripe webhook signature verification failed', { error: err.message });
    return res.status(400).send(`Webhook Error: ${err.message}`);
  }

  logger.info('Stripe webhook received', { type: event.type, id: event.id });

  try {
    // Handle the event
    switch (event.type) {
      case 'payment_intent.succeeded':
        await handlePaymentSuccess(event.data.object);
        break;

      case 'payment_intent.payment_failed':
        await handlePaymentFailed(event.data.object);
        break;

      case 'invoice.payment_succeeded':
        await handleInvoicePaymentSuccess(event.data.object);
        break;

      case 'customer.subscription.created':
        await handleSubscriptionCreated(event.data.object);
        break;

      case 'customer.subscription.updated':
        await handleSubscriptionUpdated(event.data.object);
        break;

      case 'customer.subscription.deleted':
        await handleSubscriptionCancelled(event.data.object);
        break;

      default:
        logger.info('Unhandled event type', { type: event.type });
    }

    res.json({ received: true });
  } catch (err) {
    logger.error('Error processing Stripe webhook', {
      error: err.message,
      stack: err.stack,
      eventType: event.type
    });
    res.status(500).json({ error: 'Webhook processing failed' });
  }
});

async function handlePaymentSuccess(paymentIntent) {
  logger.info('Payment succeeded', {
    id: paymentIntent.id,
    amount: paymentIntent.amount
  });

  // Save to database
  await paymentService.recordPayment({
    externalId: paymentIntent.id,
    provider: 'stripe',
    customerEmail: paymentIntent.receipt_email,
    amount: paymentIntent.amount,
    currency: paymentIntent.currency.toUpperCase(),
    status: 'succeeded',
    description: paymentIntent.description,
    metadata: paymentIntent.metadata
  });

  // Send notification
  await notificationService.sendPaymentNotification({
    type: 'success',
    provider: 'Stripe',
    amount: paymentIntent.amount / 100,
    currency: paymentIntent.currency.toUpperCase(),
    customer: paymentIntent.receipt_email
  });
}

async function handlePaymentFailed(paymentIntent) {
  logger.warn('Payment failed', {
    id: paymentIntent.id,
    error: paymentIntent.last_payment_error?.message
  });

  await paymentService.recordPayment({
    externalId: paymentIntent.id,
    provider: 'stripe',
    customerEmail: paymentIntent.receipt_email,
    amount: paymentIntent.amount,
    currency: paymentIntent.currency.toUpperCase(),
    status: 'failed',
    description: paymentIntent.description,
    metadata: {
      ...paymentIntent.metadata,
      error: paymentIntent.last_payment_error?.message
    }
  });

  await notificationService.sendPaymentNotification({
    type: 'failed',
    provider: 'Stripe',
    amount: paymentIntent.amount / 100,
    currency: paymentIntent.currency.toUpperCase(),
    customer: paymentIntent.receipt_email,
    error: paymentIntent.last_payment_error?.message
  });
}

async function handleInvoicePaymentSuccess(invoice) {
  logger.info('Invoice payment succeeded', {
    id: invoice.id,
    subscription: invoice.subscription
  });

  // Update subscription status if applicable
  if (invoice.subscription) {
    await paymentService.updateSubscriptionStatus(
      invoice.subscription,
      'active'
    );
  }
}

async function handleSubscriptionCreated(subscription) {
  logger.info('Subscription created', {
    id: subscription.id,
    customer: subscription.customer
  });

  await paymentService.recordSubscription({
    externalId: subscription.id,
    provider: 'stripe',
    customerEmail: subscription.customer_email,
    planName: subscription.items.data[0]?.plan.nickname || 'Unknown',
    amount: subscription.items.data[0]?.plan.amount || 0,
    currency: subscription.currency.toUpperCase(),
    interval: subscription.items.data[0]?.plan.interval || 'month',
    status: subscription.status,
    currentPeriodStart: new Date(subscription.current_period_start * 1000),
    currentPeriodEnd: new Date(subscription.current_period_end * 1000)
  });

  await notificationService.sendSubscriptionNotification({
    type: 'created',
    provider: 'Stripe',
    customer: subscription.customer_email,
    plan: subscription.items.data[0]?.plan.nickname
  });
}

async function handleSubscriptionUpdated(subscription) {
  logger.info('Subscription updated', {
    id: subscription.id,
    status: subscription.status
  });

  await paymentService.updateSubscription(subscription.id, {
    status: subscription.status,
    currentPeriodEnd: new Date(subscription.current_period_end * 1000)
  });
}

async function handleSubscriptionCancelled(subscription) {
  logger.info('Subscription cancelled', {
    id: subscription.id
  });

  await paymentService.updateSubscription(subscription.id, {
    status: 'cancelled',
    cancelledAt: new Date()
  });

  await notificationService.sendSubscriptionNotification({
    type: 'cancelled',
    provider: 'Stripe',
    customer: subscription.customer_email
  });
}

module.exports = router;
