param([string]$WindowTitle)
Add-Type -AssemblyName PresentationFramework,PresentationCore,WindowsBase
$form=New-Object Windows.Window
$form.Title=$WindowTitle; $form.Width=520; $form.Height=220
$panel=New-Object Windows.Controls.StackPanel
$panel.Margin=New-Object Windows.Thickness 15
$box=New-Object Windows.Controls.TextBox
$box.Height=80; $box.AcceptsReturn=$true
[Windows.Automation.AutomationProperties]::SetName($box,'Audit editor')
$button=New-Object Windows.Controls.Button
$button.Content='Audit action'; $button.Height=30
$button.Add_Click({$box.Text='CLICKED'})
[void]$panel.Children.Add($box); [void]$panel.Children.Add($button)
$form.Content=$panel
$form.Add_ContentRendered({[void]$box.Focus()})
[void]$form.ShowDialog()
