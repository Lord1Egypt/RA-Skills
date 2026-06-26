# Pet Skill Troubleshooting

This file extends the troubleshooting summary in [SKILL.md](../SKILL.md) and is organized by "most common failure branches" for quick lookups.

## 1) `Invalid body: ak, nickName, cmd required.`

- Verify the `POST /robot/skill/pet/cmd` body contains `ak`, `nickName`, and `cmd`.
- The field name must be exactly `nickName` (uppercase `N`), not `nickname`.
- `cmd` must be a non-empty string.
- `data` can be omitted; if present, it must be an object (not an array or string).

## 2) `Device is not pet (FAMIBOT)…`

Meaning: the device is not classified as **FAMIBOT**, so the request is rejected and the hint suggests switching to `/robot/skill/ctl`.

Path to resolution:

- **First check whether `product_category` is present in `deviceList`**.
  If it exists and equals `FAMIBOT`, this error typically should not be triggered.
- **Confirm `nickName` matches the right device.**
  Use a more precise / unique substring (or temporarily rename the device in-app) and retry — avoid accidentally matching a non-pet device.
- **Still not recognized as a pet device.**
  Send the device information from the response (e.g. `deviceName`, `nick`) to a maintainer for investigation.

## 3) `command not enabled`

The requested `cmd` is outside this skill's supported command set.

Resolution:

- Use only the **Queries / Settings / Control** commands listed in [SKILL.md](../SKILL.md).
- If the user needs something outside that list, ask a maintainer — do not guess alternate `cmd` names.

## 4) Token errors like 4504

Meaning: the user-side token bound to the AK is invalid or auth failed (commonly when the AK is rotated, permissions are revoked, or environments are mixed up).

Resolution:

- Check / rotate the AK on the Open Platform.
- Make sure the request hits the correct Open Platform domain (Mainland China `open.ecovacs.cn` / non-China regions `open.ecovacs.com`).

## 5) 3003 / permission denied / device not found

Resolution:

- Use `/robot/skill/deviceList` to confirm the device is in the list.
- `nickName` is a fuzzy fragment — keep it unique; if there are duplicates, use a more precise fragment (e.g. include digits or the full nickname).
- For repeated names, temporarily rename the device or use a more unique fragment.

## 6) `set*` arguments have no effect

Things to check:

- Use the recommended input fields (see [schema.md](schema.md)).

## 7) Display action returns OK but the pet only makes sound or does not move

Meaning: the pet may be asleep / eyes closed. In that state, the gateway can return OK while physical display actions are silently ignored.

Resolution:

- The helper script now guards `display` commands automatically: it calls `getCamera`, sends `setCamera {"enable":1}` when `enable != 1`, polls until the pet is awake, sends `setWorkMode {"mode":"standard"}`, and then sends the action.
- If wake-up fails, confirm the device is online and not in a protection state such as docked/charging or firmware-level motion lock.
- Manually wake the pet in the app, then retry the display action.
