#!/bin/bash

# ==============================================================================
# 数据清洗和匿名化脚本 (Shell 版本)
# 功能：对传入的文件名字符串进行匿名化处理。
# ==============================================================================

invoke_data_cleaning_anonymization() {
    local input_string="$1"
    local file_name_part=""
    local extension_part=""
    local anonymized_name=""
    local length=0
    local first_char=""
    local last_char=""
    local mask_length=0
    local masks=""

    if [[ "$input_string" =~ ^(.+?)(\.[^.]+)$ ]]; then
        file_name_part="${BASH_REMATCH[1]}"
        extension_part="${BASH_REMATCH[2]}"

        length=${#file_name_part}

        if [ "$length" -le 2 ]; then
            anonymized_name="$file_name_part"
        else
            first_char="${file_name_part:0:1}"
            last_char="${file_name_part: -1}"
            mask_length=$((length - 2))
            
            masks=$(printf '%*s' "$mask_length" | tr ' ' '*')
            anonymized_name="${first_char}${masks}${last_char}"
        fi

        echo "${anonymized_name}${extension_part}"
    else
        length=${#input_string}
        if [ "$length" -le 2 ]; then
            echo "$input_string"
        else
            first_char="${input_string:0:1}"
            last_char="${input_string: -1}"
            mask_length=$((length - 2))
            
            masks=$(printf '%*s' "$mask_length" | tr ' ' '*')
            echo "${first_char}${masks}${last_char}"
        fi
    fi
}
