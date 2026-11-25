# Retell

Retell runs functions before and after each call. They are set in the dashboard under the agent's workflow
(they are not part of the public API).

## 1. Pre-call function (HTTP request)

- Method: `GET`
- URL: `https://linepref.byronwebstudio.com.au/v1/check?number={{user_number}}`
- Output tab: map response field `advice` to a dynamic variable named `linepref_advice`, and `booking.url` to
  `linepref_booking_url`.

A pre-call function cannot cancel the call, so do the gating in one of two ways:

- **Best:** call the same URL from your own code before you create the call, and skip the call when `advice`
  is `use_link` or `do_not_call`.
- **Dashboard only:** add this to the top of the agent prompt:

  > If `{{linepref_advice}}` is `do_not_call`, say "Sorry to bother you, goodbye" and end the call
  > immediately. If it is `use_link`, end the call immediately without speaking.

## 2. Opt-out disclosure

Put this in the agent's opening line:

> This is an automated assistant. To stop calls from us, press 9 at any time. To stop automated assistant
> calls from all participating callers, press 8.

## 3. Opt-out capture (custom function, mid-call)

Add a custom function named `record_opt_out`:

- Method: `POST`, URL: `https://linepref.byronwebstudio.com.au/v1/optout`
- Description: "Call when the person presses 9 or 8, or asks to stop being called."
- Parameters: `number` (string, use `{{user_number}}`), `scope` (string: `caller` for 9 or a spoken request,
  `all` for 8)

If your agent is set up to receive key presses, map 9 and 8 as above. If it is not, change the opening line
to a spoken version ("say stop calling at any time") and keep the same function.

## 4. Post-call function (HTTP request)

- Method: `POST`, URL: `https://linepref.byronwebstudio.com.au/v1/outcome`
- Body: `{"number": "{{user_number}}", "code": "<one of the codes below>"}`

Add a post-call analysis field named `linepref_code` with these allowed values, and send it as `code`:
`connected_human`, `connected_ai`, `voicemail`, `no_answer`, `busy`, `wrong_number`, `closed`, `refused_ai`,
`booked`, `info_obtained`, `opted_out`.
