---
name: garmin-realtime-tracker
description: >
  Facilitates real-time tracking and automated data delivery from Garmin devices.
  Use this skill when the user needs to access live location, activity data, or sensor streams
  from Garmin wearables and push this data to an external system automatically.
---

# Garmin Real-time Tracker

## Overview

This skill provides guidance and methods for achieving real-time tracking and automated data delivery from Garmin devices, focusing on solutions for live location, activity data, and sensor streams.

## Core Capabilities for Real-time Data

Garmin offers several pathways for accessing data, with varying degrees of real-time capability. Understanding these distinctions is crucial for selecting the appropriate integration method.

### 1. On-Device Real-time (Garmin Connect IQ)

Garmin Connect IQ allows developers to create applications that run directly on Garmin devices. These applications can access real-time sensor data, including GPS coordinates and activity metrics, directly from the device's sensors.

*   **Mechanism:** Develop a custom Connect IQ app using the `Toybox.Position` module for location events and `ActivityMonitor` for activity metrics [1].
*   **Real-time Data Access:** The app can continuously receive location updates (`Position.enableLocationEvents(Position.LOCATION_CONTINUOUS, method(:onPosition))`) and access current activity information (`ActivityMonitor.getInfo()`) [1].
*   **Automated Delivery:** To push this data off-device in real-time, the Connect IQ app must use `Communications.makeWebRequest()` to send data to an external server frequently. This requires careful management of device battery life and network connectivity.
*   **Use Case:** Ideal for highly customized on-device experiences that need immediate sensor data and can manage frequent web requests for external data push.

### 2. Mobile App Real-time Streaming (Garmin Health Companion SDK)

The Garmin Health Companion SDK enables direct integration with Garmin wearables via Bluetooth, allowing mobile applications (Android/iOS) to tap into real-time sensor streams.

*   **Mechanism:** Integrate the Companion SDK into a mobile application to receive live streams of heart rate, stress scores, accelerometer data, and more [6].
*   **Real-time Data Access:** Provides instant access to current activity data (e.g., step counts) and subscribes to live sensor streams.
*   **Automated Delivery:** The mobile app acts as an intermediary, receiving real-time data from the wearable and then pushing it to a backend server using standard mobile networking capabilities (e.g., HTTP POST requests, WebSockets).
*   **Use Case:** Best for mobile-centric solutions requiring live sensor data for immediate feedback or analysis, where the mobile device can handle data aggregation and forwarding.

### 3. Post-Sync Data (Garmin Connect Activity & Health APIs)

The Garmin Connect Developer Program offers Activity and Health APIs for cloud-to-cloud integrations. These APIs provide access to detailed fitness and health data after a user syncs their device with Garmin Connect.

*   **Mechanism:** RESTful APIs that allow platforms to retrieve user data from Garmin Connect [3, 4, 5].
*   **Real-time Data Access:** Not truly real-time for live tracking. Data becomes available via the API *after* the user's device has synced with Garmin Connect. This means there can be a delay between the activity occurring and the data being accessible.
*   **Automated Delivery:** Supports both Ping/Pull (your system requests data) and Push (Garmin sends data to your registered callback URLs via webhooks when new data is available) architectures [4, 5]. Webhooks provide automated notifications but are not for live, continuous streaming.
*   **Use Case:** Suitable for applications that require historical data, daily summaries, or near real-time updates (minutes to hours, depending on sync frequency) rather than second-by-second live streams.

### 4. LiveTrack (Unofficial/Community Solutions)

Garmin's LiveTrack feature provides a real-time view of a user's location during an activity for friends and family. However, Garmin does not provide an official public API for third-party developers to access LiveTrack data directly.

*   **Mechanism:** Unofficial community projects (e.g., `renarsvilnis/garmin-livetrack` [2]) attempt to interface with the LiveTrack web service by scraping or reverse-engineering. These often rely on session IDs and tokens.
*   **Real-time Data Access:** Can provide location updates, typically every few seconds (e.g., 4 seconds [2]).
*   **Automated Delivery:** Requires custom implementation to parse and forward the data obtained from these unofficial methods.
*   **Limitations:** Highly unstable and not recommended for production systems due to lack of official support, potential for breakage with Garmin's website changes, and reliance on potentially insecure methods. Use at your own risk.
*   **Use Case:** For personal projects or experimental purposes where official API limitations are a barrier and stability is not a primary concern.

## Recommendations for Real-time Implementation

*   For **true real-time sensor streams** directly from the device to a mobile app, the **Garmin Health Companion SDK** is the most robust and officially supported solution [6].
*   For **on-device processing and occasional data push**, developing a **Connect IQ app** is viable, but consider battery implications [1].
*   For **post-activity automated updates**, leverage the **Push (Webhooks)** functionality of the Garmin Connect Activity and Health APIs [4, 5].
*   **Avoid unofficial LiveTrack solutions** for critical applications due to their inherent instability and lack of support.

## Resources

This skill includes example resource directories that demonstrate how to organize different types of bundled resources:

### scripts/
Executable code (Python/Bash/etc.) that can be run directly to perform specific operations.

### references/
Documentation and reference material intended to be loaded into context to inform Manus's process and thinking.

### templates/
Files not intended to be loaded into context, but rather used within the output Manus produces.

---

## References
[1] [Garmin Connect IQ - Location Data and Events, Activity Monitoring API](https://developer.garmin.com/connect-iq/core-topics/positioning) & [ActivityMonitor.Info Fields](https://developer.garmin.com/connect-iq/api-docs/Toybox/ActivityMonitor/Info.html)
[2] [GitHub - renarsvilnis/garmin-livetrack](https://github.com/renarsvilnis/garmin-livetrack)
[3] [Garmin Connect Developer Program - Overview](https://developer.garmin.com/gc-developer-program/overview/)
[4] [Garmin Connect Developer Program - Activity API](https://developer.garmin.com/gc-developer-program/activity-api/)
[5] [Garmin Connect Developer Program - Health API](https://developer.garmin.com/gc-developer-program/health-api/)
[6] [Garmin Health SDKs - Overview](https://developer.garmin.com/health-sdk/overview/)
