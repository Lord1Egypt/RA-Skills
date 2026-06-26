#!/usr/bin/expect -f
# 自动配置 SSH Key 到服务器

set timeout 10
set server_ip "192.168.1.168"
set server_user "root"
set server_password "zhangjiamin"
set ssh_key "~/.ssh/server_deploy.pub"

spawn ssh-copy-id -i $ssh_key $server_user@$server_ip

expect {
    "yes/no" {
        send "yes\r"
        expect "password:"
        send "$server_password\r"
    }
    "password:" {
        send "$server_password\r"
    }
}

expect {
    "password:" {
        send "$server_password\r"
    }
    eof
}

expect eof
puts "\n✅ SSH Key 配置完成！"
