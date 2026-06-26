function buildNotification(update, options = {}) {
  const target = update.follow || {};
  const latestUpload = update.latest_upload || {};
  const latestUpdate = update.latest_update || {};

  return {
    kind: "creator_update",
    delivery_target: options.delivery_target || null,
    channel_id: target.channel_id || null,
    title: latestUpdate.headline || latestUpload.title || "New creator update",
    text: latestUpdate.summary || latestUpload.title || "New upload detected",
    markdown: latestUpdate.markdown || latestUpload.title || "New upload detected",
    video_url: latestUpload.video_url || null,
    published_at: latestUpload.published_at || null,
    metadata: {
      creator_title: target.title || latestUpload.channel_title || null,
      video_id: latestUpload.video_id || null,
      source_input: target.source_input || null,
    },
  };
}

function getDeliveryAdapter(context = {}) {
  if (typeof context.deliver === "function") {
    return {
      kind: "context.deliver",
      send: (notification) => context.deliver(notification),
    };
  }

  if (typeof context.notify === "function") {
    return {
      kind: "context.notify",
      send: (notification) => context.notify(notification),
    };
  }

  if (typeof context.sendMessage === "function") {
    return {
      kind: "context.sendMessage",
      send: (notification) =>
        context.sendMessage(notification.markdown || notification.text, notification),
    };
  }

  if (context.channel && typeof context.channel.send === "function") {
    return {
      kind: "context.channel.send",
      send: (notification) =>
        context.channel.send(notification.markdown || notification.text, notification),
    };
  }

  if (context.channels && typeof context.channels.send === "function") {
    return {
      kind: "context.channels.send",
      send: (notification) =>
        context.channels.send(notification.delivery_target, notification),
    };
  }

  return null;
}

async function dispatchNotifications(notifications, options = {}, context = {}) {
  const adapter = getDeliveryAdapter(context);

  if (!adapter) {
    return {
      ok: false,
      adapter: null,
      delivered_count: 0,
      failed_count: 0,
      deliveries: [],
      message: "No runtime delivery adapter is available in the current skill context.",
    };
  }

  const deliveries = [];

  for (const notification of notifications) {
    try {
      const result = await adapter.send({
        ...notification,
        delivery_target: options.delivery_target || notification.delivery_target || null,
      });

      deliveries.push({
        ok: true,
        adapter: adapter.kind,
        notification,
        result: result ?? null,
      });
    } catch (error) {
      deliveries.push({
        ok: false,
        adapter: adapter.kind,
        notification,
        error: error.message || "Delivery failed.",
      });
    }
  }

  const deliveredCount = deliveries.filter((item) => item.ok).length;
  const failedCount = deliveries.length - deliveredCount;

  return {
    ok: failedCount === 0,
    adapter: adapter.kind,
    delivered_count: deliveredCount,
    failed_count: failedCount,
    deliveries,
    message:
      failedCount === 0
        ? `Delivered ${deliveredCount} notification(s).`
        : `Delivered ${deliveredCount} notification(s), ${failedCount} failed.`,
  };
}

module.exports = {
  buildNotification,
  dispatchNotifications,
  getDeliveryAdapter,
};
