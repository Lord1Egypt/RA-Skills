import { formatLocalIso } from "./utils.js";

export function getSystemInfo(now = new Date()) {
  const timezone = Intl.DateTimeFormat().resolvedOptions().timeZone ?? "unknown";
  const hour = now.getHours();
  const isLateNight = hour >= 23 || hour < 5;

  return {
    current_time: formatLocalIso(now),
    timezone,
    local_hour: hour,
    is_late_night: isLateNight
  };
}
