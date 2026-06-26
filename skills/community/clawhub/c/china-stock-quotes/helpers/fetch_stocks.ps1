param(
    [string[]]$Codes = @("s_sh000001","s_sz399001","sh600519","sz300750")
)

$sinaUrl = "https://hq.sinajs.cn/list=" + ($Codes -join ",")
$referer = "https://finance.sina.com.cn"

try {
    $response = curl.exe -s -e $referer $sinaUrl
    $lines = $response -split "`n"
    
    foreach ($line in $lines) {
        if ($line -match 'var hq_str_(\w+)="(.+)"') {
            $fullCode = $matches[1]
            $data = $matches[2] -split ","
            
            if ($fullCode -match "^s_") {
                # Index format
                $idxName = $data[0]
                $current = [double]$data[1]
                $change = [double]$data[2]
                $changePct = [double]$data[3]
                $arrow = if ($change -ge 0) { "🟢" } else { "🔴" }
                Write-Host "$arrow $idxName`: $current`  $change ($changePct%)"
            }
            else {
                # Stock format
                $stockName = $data[0]
                $open = [double]$data[1]
                $prevClose = [double]$data[2]
                $current = [double]$data[3]
                $high = [double]$data[4]
                $low = [double]$data[5]
                $volume = [int64]$data[8]
                $amount = [double]$data[9]
                
                $change = $current - $prevClose
                $changePct = if ($prevClose -ne 0) { $change / $prevClose * 100 } else { 0 }
                $arrow = if ($change -ge 0) { "🟢" } else { "🔴" }
                
                Write-Host "$arrow $stockName ($fullCode)`:$current`  $("{0:+0.00;-#0.00}" -f $change) ($("{0:+0.00;-#0.00}" -f $changePct)%)"
                Write-Host "   开:$open` 高:$high` 低:$low` 昨收:$prevClose"
                Write-Host "   量:$("{0:N0}" -f $volume)手` 额:$("{0:N0}" -f $amount)元"
            }
        }
    }
}
catch {
    Write-Host "查询失败: $_"
}
