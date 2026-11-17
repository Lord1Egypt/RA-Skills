# desktop-notify for Windows: 系统提示音 + WinRT Toast 原生通知
param(
    [string]$Message = "任务完成，请查看",
    [string]$Title = "WorkBuddy"
)

# 1. 播放系统完成音
[System.Media.SystemSounds]::Asterisk.Play()

# 2. 弹出 WinRT Toast 通知
$template = [Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime]::GetTemplateContent([Windows.UI.Notifications.ToastTemplateType, Windows.UI.Notifications, ContentType = WindowsRuntime]::ToastText01)
$textNodes = $template.GetElementsByTagName("text")
$textNodes.Item(0).AppendChild($template.CreateTextNode("$Title : $Message")) | Out-Null
$toast = [Windows.UI.Notifications.ToastNotification, Windows.UI.Notifications, ContentType = WindowsRuntime]::New($template)
[Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier($Title).Show($toast)
Write-Host "通知已发送 (Windows)"
