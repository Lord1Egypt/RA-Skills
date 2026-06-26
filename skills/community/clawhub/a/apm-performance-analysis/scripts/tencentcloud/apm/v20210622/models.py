# -*- coding: utf8 -*-
# Copyright (c) 2017-2025 Tencent. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import warnings

from tencentcloud.common.abstract_model import AbstractModel


class APMKVItem(AbstractModel):
    r"""APM 通用 KV 结构

    """

    def __init__(self):
        r"""
        :param _Key: Key 值定义
        :type Key: str
        :param _Value: Value 值定义
        :type Value: str
        """
        self._Key = None
        self._Value = None

    @property
    def Key(self):
        r"""Key 值定义
        :rtype: str
        """
        return self._Key

    @Key.setter
    def Key(self, Key):
        self._Key = Key

    @property
    def Value(self):
        r"""Value 值定义
        :rtype: str
        """
        return self._Value

    @Value.setter
    def Value(self, Value):
        self._Value = Value


    def _deserialize(self, params):
        self._Key = params.get("Key")
        self._Value = params.get("Value")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class MCPMessage(AbstractModel):
    r"""MCP服务响应

    """

    def __init__(self):
        r"""
        :param _Result: <p>MCP响应数据</p>
        :type Result: str
        """
        self._Result = None

    @property
    def Result(self):
        r"""<p>MCP响应数据</p>
        :rtype: str
        """
        return self._Result

    @Result.setter
    def Result(self, Result):
        self._Result = Result


    def _deserialize(self, params):
        self._Result = params.get("Result")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class SendMCPMessageRequest(AbstractModel):
    r"""SendMCPMessage请求参数结构体

    """

    def __init__(self):
        r"""
        :param _Method: <p>mcp方法值</p><p>枚举值：</p><ul><li>tools/list： 列举当前mcp支持的工具列表</li><li>tools/call： 调用具体工具</li><li>ping： ping</li></ul>
        :type Method: str
        :param _ToolName: <p>Method=tools/call 时，要调用的工具名称</p>
        :type ToolName: str
        :param _Arguments: <p>Method=tools/call 时，工具参数</p>
        :type Arguments: list of APMKVItem
        """
        self._Method = None
        self._ToolName = None
        self._Arguments = None

    @property
    def Method(self):
        r"""<p>mcp方法值</p><p>枚举值：</p><ul><li>tools/list： 列举当前mcp支持的工具列表</li><li>tools/call： 调用具体工具</li><li>ping： ping</li></ul>
        :rtype: str
        """
        return self._Method

    @Method.setter
    def Method(self, Method):
        self._Method = Method

    @property
    def ToolName(self):
        r"""<p>Method=tools/call 时，要调用的工具名称</p>
        :rtype: str
        """
        return self._ToolName

    @ToolName.setter
    def ToolName(self, ToolName):
        self._ToolName = ToolName

    @property
    def Arguments(self):
        r"""<p>Method=tools/call 时，工具参数</p>
        :rtype: list of APMKVItem
        """
        return self._Arguments

    @Arguments.setter
    def Arguments(self, Arguments):
        self._Arguments = Arguments


    def _deserialize(self, params):
        self._Method = params.get("Method")
        self._ToolName = params.get("ToolName")
        if params.get("Arguments") is not None:
            self._Arguments = []
            for item in params.get("Arguments"):
                obj = APMKVItem()
                obj._deserialize(item)
                self._Arguments.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class SendMCPMessageResponse(AbstractModel):
    r"""SendMCPMessage返回参数结构体

    """

    def __init__(self):
        r"""
        :param _MCPMessage: <p>MCP服务响应信息</p>
        :type MCPMessage: :class:`tencentcloud.apm.v20210622.models.MCPMessage`
        :param _RequestId: 唯一请求 ID，由服务端生成，每次请求都会返回（若请求因其他原因未能抵达服务端，则该次请求不会获得 RequestId）。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._MCPMessage = None
        self._RequestId = None

    @property
    def MCPMessage(self):
        r"""<p>MCP服务响应信息</p>
        :rtype: :class:`tencentcloud.apm.v20210622.models.MCPMessage`
        """
        return self._MCPMessage

    @MCPMessage.setter
    def MCPMessage(self, MCPMessage):
        self._MCPMessage = MCPMessage

    @property
    def RequestId(self):
        r"""唯一请求 ID，由服务端生成，每次请求都会返回（若请求因其他原因未能抵达服务端，则该次请求不会获得 RequestId）。定位问题时需要提供该次请求的 RequestId。
        :rtype: str
        """
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        if params.get("MCPMessage") is not None:
            self._MCPMessage = MCPMessage()
            self._MCPMessage._deserialize(params.get("MCPMessage"))
        self._RequestId = params.get("RequestId")