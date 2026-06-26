# Email Templates

All emails sent from: **[Business Name]** <[business-email]>

## Enquiry Acknowledgement

**Subject:** Your Appointment Enquiry - [SERVICE]

```html
<div style="font-family: Arial, sans-serif; color: #333; line-height: 1.6;">
  <p>Dear [NAME],</p>
  <p>Thank you for your appointment enquiry with <strong>[BUSINESS_NAME]</strong>.</p>
  <p><strong>Requested Date:</strong> [DATE]<br>
  <strong>Requested Time:</strong> [TIME]<br>
  <strong>Service:</strong> [SERVICE]<br>
  <strong>Phone:</strong> [PHONE]</p>
  <p>Your enquiry has been received. Our team will contact you shortly to confirm availability.</p>
  <hr style="margin: 25px 0;">
  [BOOKING_POLICY]
  <hr style="margin: 25px 0;">
  <p style="text-align: center; color: red; font-weight: bold;">
    Please note: This email is an acknowledgement of your enquiry only.<br>
    A booking confirmation will follow shortly.
  </p>
  <p>We look forward to welcoming you.<br>
  Please do not hesitate to reply if you have any questions.</p>
  <p><strong>Warm regards,</strong><br>
  <strong>[BUSINESS_NAME]</strong></p>
</div>
```

## Confirmation

**Subject:** Your Appointment is Confirmed

```html
<div style="font-family: Arial, sans-serif; color: #333; line-height: 1.6;">
  <p>Dear [NAME],</p>
  <p>We are pleased to confirm your appointment with <strong>[BUSINESS_NAME]</strong>.</p>
  <p><strong>Appointment Date:</strong> [DATE]<br>
  <strong>Appointment Time:</strong> [TIME]<br>
  <strong>Service:</strong> [SERVICE]<br>
  <strong>Phone:</strong> [PHONE]</p>
  <p>Your appointment has been confirmed. Please find your calendar invite attached.</p>
  <hr style="margin: 25px 0;">
  [BOOKING_POLICY]
  <hr style="margin: 25px 0;">
  <p style="text-align: center; color: red; font-weight: bold;">
    This email confirms your appointment.
  </p>
  <p>We look forward to welcoming you.</p>
  <p><strong>Warm regards,</strong><br>
  <strong>[BUSINESS_NAME]</strong></p>
</div>
```

## Cancellation

**Subject:** Appointment Cancelled

```html
<div style="font-family: Arial, sans-serif; color: #333; line-height: 1.6;">
  <p>Dear [NAME],</p>
  <p>Your appointment with <strong>[BUSINESS_NAME]</strong> has been cancelled.</p>
  <p><strong>Service:</strong> [SERVICE]<br>
  <strong>Original Date:</strong> [DATE]<br>
  <strong>Original Time:</strong> [TIME]</p>
  <p>If you would like to rebook, please visit our website or contact us directly.</p>
  <p><strong>Warm regards,</strong><br>
  <strong>[BUSINESS_NAME]</strong></p>
</div>
```

## Appointment Reminder

**Subject:** Reminder: Your Appointment Tomorrow - [SERVICE]

```html
<div style="font-family: Arial, sans-serif; color: #333; line-height: 1.6;">
  <p>Dear [NAME],</p>
  <p>This is a friendly reminder that you have an upcoming appointment with
  <strong>[BUSINESS_NAME]</strong>.</p>
  <p><strong>Date:</strong> [DATE]<br>
  <strong>Time:</strong> [TIME]<br>
  <strong>Service:</strong> [SERVICE]</p>
  <p>We look forward to seeing you!</p>
  <!-- OPTIONAL: Cancel/reschedule block. Include ONLY if the business allows it. -->
  <!-- [REMINDER_CHANGE_BLOCK] -->
  <hr style="margin: 25px 0;">
  <!-- OPTIONAL: Policy footer. Include if the business wants a policy reminder. -->
  <!-- [REMINDER_POLICY_FOOTER] -->
  <p><strong>Warm regards,</strong><br>
  <strong>[BUSINESS_NAME]</strong></p>
</div>
```

### Optional: Cancel/reschedule block

Include this block **only** if the business allows changes within 24 hours.
Remove entirely if the business enforces a no-changes policy close to appointments.

```html
<p>Need to make changes? Please contact us as soon as possible by replying to
this email or calling <strong>[PHONE_NUMBER]</strong>.</p>
```

### Optional: Policy footer

Include when the business wants to reinforce their policy in the reminder.
Customise the text per business.

Example (strict policy):

```html
<p style="font-size: 0.9em; color: #666;">
  <strong>Please note:</strong> Cancellations within 48 hours of your appointment
  or no-shows will incur a charge as per our booking policy.
</p>
```

Example (flexible policy):

```html
<p style="font-size: 0.9em; color: #666;">
  Need to reschedule? No problem — just let us know at least 2 hours before
  your appointment time.
</p>
```

## Booking Policy Block

Replace `[BOOKING_POLICY]` with the business-specific policy. Example:

```html
<h3 style="color: #b8926a;">Booking Policy</h3>
<p>
  - A non-refundable deposit is required to secure your booking.<br>
  - Appointments may be rescheduled once with 48 hours' notice.<br>
  - Cancellations within 48 hours or no-shows forfeit the deposit.<br>
  - Please arrive on time. Late arrivals may need rescheduling.<br>
  - Frequent last-minute changes may affect future booking availability.
</p>
```

## Sending via SMTP

Credentials must be stored as environment variables in `openclaw.json` under `env`:
- `SMTP_HOST` (e.g. smtp.gmail.com)
- `SMTP_USER` (the sending email address)
- `SMTP_PASSWORD` (app password, never a primary password)

Use the agent's standard email-sending capability with these environment variables.
Build the email with MIME headers for HTML content and .ics attachment.
