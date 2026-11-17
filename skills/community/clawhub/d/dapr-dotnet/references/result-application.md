# 统一返回结构与 Application 层模板

> 摘自 dapr-dotnet 技能 v1.0.0「Result Pattern / Application」章节。包含：ApiResult 返回体家族、IBaseService/BaseService 泛型服务基类及示例。

## 一、ApiResult 返回体

```csharp
// Common/ApiResult.cs
public class BaseResult
{
    /// <summary>
    /// 响应码
    /// </summary>
    [NotNull]
    public virtual HttpStatusCode Code { get; set; }


    /// <summary>
    /// 响应成功
    /// </summary>
    /// <returns></returns>
    public virtual void Success()
    {
        Code = HttpStatusCode.OK;
    }

    /// <summary>
    /// 响应失败
    /// </summary>
    /// <param name="message"></param>
    public virtual void Failed()
    {
        Code = HttpStatusCode.InternalServerError;
    }
}

/// <summary>
/// API返回结果结构
/// </summary>
public class ApiResult : BaseResult
{
    public ApiResult()
    {
        Success();
    }

    private string _Message = string.Empty;
    private string _Data = string.Empty;
    private byte[] _Base64Data;
    private string _ModelType = string.Empty;

    /// <summary>
    /// 消息提示
    /// </summary>
    public string Message { get => _Message; set => _Message = value; }
    /// <summary>
    /// 数据源
    /// </summary>
    public string Data { get => _Data; set => _Data = value; }
    /// <summary>
    /// 数据源模型
    /// </summary>
    public string ModelType { get => _ModelType; set => _ModelType = value; }
    /// <summary>
    /// Base64数据源
    /// </summary>
    public byte[] Base64Data { get => _Base64Data; set => _Base64Data = value; }


    /// <summary>
    /// 响应成功
    /// </summary>
    /// <param name="message">消息</param>
    public void Success(string message)
    {
        base.Success();
        _Message = message;
    }

    /// <summary>
    /// 响应成功
    /// </summary>
    /// <param name="data">数据</param>
    public void Success(dynamic data)
    {
        base.Success();

        _Data = JsonSerializer.Serialize(data, new JsonSerializerOptions
        {
            Encoder = JavaScriptEncoder.Create(UnicodeRanges.All)
        });

        _ModelType = GetDataType(data);
    }


    /// <summary>
    /// 响应成功
    /// </summary>
    /// <param name="data">数据</param>
    /// <param name="message">消息</param>
    public void Success(dynamic data, string message)
    {
        base.Success();
        _Message = message;
        _Data = JsonSerializer.Serialize(data, new JsonSerializerOptions
        {
            Encoder = JavaScriptEncoder.Create(UnicodeRanges.All)
        });
        _ModelType = GetDataType(data);
    }


    /// <summary>
    /// 响应成功
    /// </summary>
    /// <param name="dataList">数据</param>
    public void Success<T>(List<T> dataList)
    {
        base.Success();

        if (dataList != null && dataList.Any())
        {
            _Data = JsonSerializer.Serialize(dataList, new JsonSerializerOptions
            {
                Encoder = JavaScriptEncoder.Create(UnicodeRanges.All)
            });
            _ModelType = GetDataType(dataList);
        }
        else
        {
            _Data = string.Empty;
            _ModelType = string.Empty;
        }
    }

    /// <summary>
    /// 响应成功
    /// </summary>
    /// <param name="dataList">数据</param>
    /// <param name="message">消息</param>
    public void Success<T>(List<T> dataList, string message)
    {
        base.Success();
        _Message = message;
        if (dataList != null && dataList.Any())
        {
            _Data = JsonSerializer.Serialize(dataList, new JsonSerializerOptions
            {
                Encoder = JavaScriptEncoder.Create(UnicodeRanges.All)
            });
            _ModelType = GetDataType(dataList);
        }
        else
        {
            _Data = string.Empty;
            _ModelType = string.Empty;
        }
    }

    /// <summary>
    /// 响应失败
    /// </summary>
    /// <param name="message"></param>
    public void Failed(string message)
    {
        base.Failed();
        _Message = message;
    }

    /// <summary>
    /// 响应失败
    /// </summary>
    /// <param name="ex"></param>
    public void Failed(Exception ex)
    {
        base.Failed();
        _Message = ex.Message.ToString();
    }

    /// <summary>
    /// 响应失败
    /// </summary>
    /// <param name="httpStatusCode"></param>
    /// <param name="message"></param>
    public void Failed(HttpStatusCode httpStatusCode, string message)
    {
        Code = httpStatusCode;
        _Message = message;
    }


    /// <summary>
    /// 成功
    /// </summary>
    /// <param name="dataSource">数据源</param>
    /// <param name="code">状态码</param>
    /// <param name="message">消息提示</param>
    /// <param name="isSerialize">是否需要序列化</param>
    public static ApiResult Success(dynamic dataSource, string message = "操作成功", HttpStatusCode code = HttpStatusCode.OK, bool isSerialize = true)
    {
        return new ApiResult(dataSource, code, message, isSerialize);
    }

    /// <summary>
    /// 成功
    /// </summary>
    /// <param name="dataSourceList">数据源</param>
    /// <param name="code">状态码</param>
    /// <param name="message">消息提示</param>
    /// <param name="isSerialize">是否需要序列化</param>
    public static ApiResult Success<T>(List<T> dataSourceList, string message = "操作成功", HttpStatusCode code = HttpStatusCode.OK, bool isSerialize = true)
    {
        if (dataSourceList != null && dataSourceList.Any())
        {
            return new ApiResult(dataSourceList, code, message, isSerialize);
        }
        else
        {
            return new ApiResult(string.Empty, code, message, isSerialize);
        }
    }

    /// <summary>
    /// 失败
    /// </summary>
    /// <param name="code">状态码</param>
    /// <param name="message">消息提示</param>
    public static ApiResult Failed(string message = "操作失败", HttpStatusCode code = HttpStatusCode.InternalServerError)
    {
        return new ApiResult(string.Empty, code, message, false);
    }

    /// <summary>
    /// 响应模型
    /// </summary>
    /// <param name="dataSource">数据源</param>
    /// <param name="code">状态码</param>
    /// <param name="message">消息提示</param>
    /// <param name="isSerialize">是否需要序列化</param>
    private ApiResult(dynamic dataSource, HttpStatusCode code, string message, bool isSerialize)
    {
        if (dataSource != null && dataSource.GetType() == typeof(byte[]) && !isSerialize)
        {
            _Base64Data = dataSource;
        }
        else if (dataSource != null && dataSource?.GetType() != typeof(string) && isSerialize)
        {
            _Data = JsonSerializer.Serialize(dataSource, new JsonSerializerOptions
            {
                PropertyNamingPolicy = JsonNamingPolicy.CamelCase,
                NumberHandling = JsonNumberHandling.WriteAsString,
                Encoder = JavaScriptEncoder.Create(UnicodeRanges.All)
            });
        }
        else
        {
            _Data = dataSource;
        }
        Code = code;
        _Message = message;
        _ModelType = GetDataType(dataSource);
    }



    /// <summary>
    /// 获取返回模型的所有属性
    /// </summary>
    /// <param name="data"></param>
    /// <returns></returns>
    private static string GetDataType(dynamic data)
    {
        var str = string.Empty;

        System.Reflection.PropertyInfo[] properties = data.GetType().GetProperties();

        foreach (System.Reflection.PropertyInfo property in properties)
        {
            string propertyName = property.Name;
            string propertyType = property.PropertyType.Name;

            str += $"{propertyName} ({propertyType}),";
        }

        return !string.IsNullOrWhiteSpace(str) ? str[..^1] : str;
    }
}

/// <summary>
/// 泛型类型返回体
/// </summary>
/// <typeparam name="T"></typeparam>
public class ApiResult<T> : ApiResult
{
    /// <summary>
    /// 数据
    /// </summary>
    public T TData { get; set; }

    /// <summary>
    /// 列表的记录数
    /// </summary>
    public int Total { get; set; }
}
```

### 使用要点

- 控制器中直接使用静态工厂：`return ApiResult.Success(data);` / `return ApiResult.Failed("操作失败");`
- 列表返回走 `ApiResult.Success<T>(List<T>)`；空列表时 `Data` 为空串、`ModelType` 为空串。
- 分页/强类型场景用 `ApiResult<T>`，数据放 `TData`，总记录数放 `Total`。
- 二进制数据（`byte[]`）走 `Base64Data` 字段，不进入 `Data` 序列化。
- `Code` 为 `HttpStatusCode` 枚举；`ModelType` 由反射生成（属性名 + 类型），供前端解析数据结构。

## 二、Application 层

### IBaseService.cs

```csharp
// Application/IServices/IBaseService.cs
public interface IBaseService<T> where T : class, new()
{
    /// <summary>
    /// 添加
    /// </summary>
    /// <param name="AEntity"></param>
    /// <returns></returns>
    bool Insert(T AEntity);

    /// <summary>
    /// 添加
    /// </summary>
    /// <param name="AEntity"></param>
    /// <returns></returns>
    Task<bool> InsertAsync(T AEntity);

    /// <summary>
    /// 批量添加
    /// </summary>
    /// <param name="AList"></param>
    /// <returns></returns>
    Task<bool> InsertRangeAsync(List<T> AList);

    /// <summary>
    /// 删除
    /// </summary>
    /// <param name="AId"></param>
    /// <returns></returns>
    bool Delete(T AEntity);

    /// <summary>
    /// 删除
    /// </summary>
    /// <param name="AId"></param>
    /// <returns></returns>
    Task<bool> DeleteAsync(dynamic AId);

    /// <summary>
    /// 批量删除
    /// </summary>
    /// <param name="AIds"></param>
    /// <returns></returns>
    Task<bool> DeleteByIdsAsync(dynamic[] AIds);

    /// <summary>
    /// 更新
    /// </summary>
    /// <param name="AEntity"></param>
    /// <returns></returns>
    bool Update(T AEntity);

    /// <summary>
    /// 更新
    /// </summary>
    /// <param name="AEntity"></param>
    /// <returns></returns>
    Task<bool> UpdateAsync(T AEntity);

    /// <summary>
    /// 批量更新
    /// </summary>
    /// <param name="AList"></param>
    /// <returns></returns>
    Task<bool> UpdateRangeAsync(List<T> AList);

    /// <summary>
    /// 查询
    /// </summary>
    /// <param name="func"></param>
    /// <returns></returns>
    T Find(Expression<Func<T, bool>> func);

    /// <summary>
    /// 根据ID查询
    /// </summary>
    /// <param name="AId"></param>
    /// <returns></returns>
    Task<T> FindAsync(dynamic AId);

    /// <summary>
    /// 查询
    /// </summary>
    /// <param name="func"></param>
    /// <returns></returns>
    Task<T> FindAsync(Expression<Func<T, bool>> func);

    /// <summary>
    /// 查询
    /// </summary>
    /// <returns></returns>
    List<T> Query();

    /// <summary>
    /// 自定义查询
    /// </summary>
    /// <param name="func"></param>
    /// <returns></returns>
    List<T> Query(Expression<Func<T, bool>> func);

    /// <summary>
    /// 查询
    /// </summary>
    /// <returns></returns>
    Task<List<T>> QueryAsync();

    /// <summary>
    /// 自定义查询
    /// </summary>
    /// <param name="func"></param>
    /// <returns></returns>
    Task<List<T>> QueryAsync(Expression<Func<T, bool>> func);

    /// <summary>
    /// 分页查询
    /// </summary>
    /// <param name="APageIndex"></param>
    /// <param name="APageSize"></param>
    /// <param name="ATotal"></param>
    /// <returns></returns>
    Task<List<T>> QueryAsync(int APageIndex, int APageSize, RefAsync<int> ATotal);

    /// <summary>
    /// 自定义条件分页查询
    /// </summary>
    /// <param name="func"></param>
    /// <param name="APageIndex"></param>
    /// <param name="APageSize"></param>
    /// <param name="ATotal"></param>
    /// <returns></returns>
    Task<List<T>> QueryAsync(Expression<Func<T, bool>> func, int APageIndex, int APageSize, RefAsync<int> ATotal);

    /// <summary>
    /// 自定义条件分页查询
    /// </summary>
    /// <param name="func"></param>
    /// <param name="APageIndex"></param>
    /// <param name="APageSize"></param>
    /// <param name="ATotal"></param>
    /// <returns></returns>
    Task<List<T>> QueryAsync(Expression<Func<T, bool>> func, string orderByFields, int APageIndex, int APageSize, RefAsync<int> ATotal);

    /// <summary>
    /// 自定义条件分页查询
    /// </summary>
    /// <param name="whereExpression"></param>
    /// <param name="orderByExpression"></param>
    /// <param name="order"></param>
    /// <param name="APageIndex"></param>
    /// <param name="APageSize"></param>
    /// <param name="ATotal"></param>
    /// <returns></returns>
    Task<List<T>> QueryAsync(Expression<Func<T, bool>> whereExpression, Expression<Func<T, object>> orderByExpression, OrderByType order, int APageIndex, int APageSize, RefAsync<int> ATotal);

    /// <summary>
    /// 开始事务
    /// </summary>
    void BeginTran();

    /// <summary>
    /// 提交
    /// </summary>
    void CommitTran();

    /// <summary>
    /// 回滚
    /// </summary>
    void RollbackTran();

    #region 执行sql

    /// <summary>
    /// 获取DataTable数据
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>DataTable</returns>
    DataTable GetDataTable(string sql, object parameters);

    /// <summary>
    /// 获取DataTable数据
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>DataTable</returns>
    DataTable GetDataTable(string sql, params SugarParameter[] parameters);

    /// <summary>
    /// 获取DataTable数据
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>DataTable</returns>
    DataTable GetDataTable(string sql, List<SugarParameter> parameters);

    /// <summary>
    /// 获取DataTable数据
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>DataTable</returns>
    Task<DataTable> GetDataTableAsync(string sql, object parameters);

    /// <summary>
    /// 获取DataTable数据
    /// </summary>
    /// <param name="ASql"></param>
    /// <param name="parameters"></param>
    /// <returns>DataTable</returns>
    Task<DataTable> GetDataTableAsync(string ASql, params SugarParameter[] parameters);

    /// <summary>
    /// 获取DataTable数据
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>DataTable</returns>
    Task<DataTable> GetDataTableAsync(string sql, List<SugarParameter> parameters);

    /// <summary>
    /// 获取DataSet数据
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>DataSet</returns>
    DataSet GetDataSetAll(string sql, object parameters);

    /// <summary>
    /// 获取DataSet数据
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>DataSet</returns>
    DataSet GetDataSetAll(string sql, params SugarParameter[] parameters);

    /// <summary>
    /// 获取DataSet数据
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>DataSet</returns>
    DataSet GetDataSetAll(string sql, List<SugarParameter> parameters);

    /// <summary>
    /// 获取DataSet数据
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>DataSet</returns>
    Task<DataSet> GetDataSetAllAsync(string sql, object parameters);

    /// <summary>
    /// 获取DataSet数据
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>DataSet</returns>
    Task<DataSet> GetDataSetAllAsync(string sql, params SugarParameter[] parameters);

    /// <summary>
    /// 获取DataSet数据
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>DataSet</returns>
    Task<DataSet> GetDataSetAllAsync(string sql, List<SugarParameter> parameters);

    /// <summary>
    /// 获取DataReader数据
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>IDataReader</returns>
    IDataReader GetDataReader(string sql, object parameters);

    /// <summary>
    /// 获取DataReader数据
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>IDataReader</returns>
    IDataReader GetDataReader(string sql, params SugarParameter[] parameters);

    /// <summary>
    /// 获取DataReader数据
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>IDataReader</returns>
    IDataReader GetDataReader(string sql, List<SugarParameter> parameters);

    /// <summary>
    /// 获取DataReader数据
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>IDataReader</returns>
    Task<IDataReader> GetDataReaderAsync(string sql, object parameters);

    /// <summary>
    /// 获取DataReader数据
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>IDataReader</returns>
    Task<IDataReader> GetDataReaderAsync(string sql, params SugarParameter[] parameters);

    /// <summary>
    /// 获取DataReader数据
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>IDataReader</returns>
    Task<IDataReader> GetDataReaderAsync(string sql, List<SugarParameter> parameters);

    /// <summary>
    /// 获取object数据
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>object</returns>
    object GetScalar(string sql, object parameters);

    /// <summary>
    /// 获取object数据
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>object</returns>
    object GetScalar(string sql, params SugarParameter[] parameters);

    /// <summary>
    /// 获取object数据
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>object</returns>
    object GetScalar(string sql, List<SugarParameter> parameters);

    /// <summary>
    /// 获取object数据
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>object</returns>
    Task<object> GetScalarAsync(string sql, object parameters);

    /// <summary>
    /// 获取object数据
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>object</returns>
    Task<object> GetScalarAsync(string sql, params SugarParameter[] parameters);

    /// <summary>
    /// 获取object数据
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>object</returns>
    Task<object> GetScalarAsync(string sql, List<SugarParameter> parameters);

    /// <summary>
    /// 执行sql返回整型
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>int</returns>
    int ExecuteCommandWithGo(string sql, params SugarParameter[] parameters);

    /// <summary>
    /// 执行sql返回整型
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>int</returns>
    int ExecuteCommand(string sql, object parameters);

    /// <summary>
    /// 执行sql返回整型
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>int</returns>
    int ExecuteCommand(string sql, params SugarParameter[] parameters);

    /// <summary>
    /// 执行sql返回整型
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>int</returns>
    int ExecuteCommand(string sql, List<SugarParameter> parameters);

    /// <summary>
    /// 执行sql返回整型
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>int</returns>
    Task<int> ExecuteCommandAsync(string sql, params SugarParameter[] parameters);

    /// <summary>
    /// 执行sql返回整型
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>int</returns>
    Task<int> ExecuteCommandAsync(string sql, object parameters);

    /// <summary>
    /// 执行sql返回整型
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>int</returns>
    Task<int> ExecuteCommandAsync(string sql, List<SugarParameter> parameters);

    /// <summary>
    /// 执行SQL返回自定义实体
    /// </summary>
    /// <typeparam name="T">实体对象</typeparam>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns></returns>
    List<T> SqlQuery<T>(string sql, object parameters = null);

    /// <summary>
    /// 执行SQL返回自定义实体
    /// </summary>
    /// <typeparam name="T">实体对象</typeparam>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns></returns>
    List<T> SqlQuery<T>(string sql, params SugarParameter[] parameters);

    /// <summary>
    /// 执行SQL返回自定义实体
    /// </summary>
    /// <typeparam name="T">实体对象</typeparam>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns></returns>
    List<T> SqlQuery<T>(string sql, List<SugarParameter> parameters);

    /// <summary>
    /// 执行SQL返回自定义实体
    /// </summary>
    /// <typeparam name="T">实体对象</typeparam>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns></returns>
    Task<List<T>> SqlQueryAsync<T>(string sql, object parameters = null);

    /// <summary>
    /// 执行SQL返回自定义实体
    /// </summary>
    /// <typeparam name="T">实体对象</typeparam>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns></returns>
    Task<List<T>> SqlQueryAsync<T>(string sql, List<SugarParameter> parameters);

    /// <summary>
    /// 执行SQL返回自定义实体
    /// </summary>
    /// <typeparam name="T">实体对象</typeparam>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns></returns>
    Task<List<T>> SqlQueryAsync<T>(string sql, params SugarParameter[] parameters);

    /// <summary>
    /// 执行SQL返回自定义实体
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="whereObj"></param>
    /// <returns></returns>
    T SqlQuerySingle<T>(string sql, object whereObj = null);

    /// <summary>
    /// 执行SQL返回自定义实体
    /// </summary>
    /// <param name="T">实体对象</typeparam>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns></returns>
    T SqlQuerySingle<T>(string sql, params SugarParameter[] parameters);

    /// <summary>
    /// 执行SQL返回自定义实体
    /// </summary>
    /// <typeparam name="T">实体对象</typeparam>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns></returns>
    T SqlQuerySingle<T>(string sql, List<SugarParameter> parameters);

    #endregion
}
```

### ITestService.cs（业务接口示例）

```csharp
// Application/IServices/ITestService.cs
public interface ITestService : IBaseService<Test>
{
}
```

### BaseService.cs

```csharp
// Application/Services/BaseService.cs
public class BaseService<T> : IBaseService<T> where T : class, new()
{
    protected IBaseRepository<T> _BaseRepository;

    public bool Delete(T AEntity)
    {
        return _BaseRepository.Delete(AEntity);
    }

    public async Task<bool> DeleteAsync(dynamic AId)
    {
        return await _BaseRepository.DeleteAsync(AId);
    }

    public async Task<bool> DeleteByIdsAsync(dynamic[] AIds)
    {
        return await _BaseRepository.DeleteByIdsAsync(AIds);
    }

    public T Find(Expression<Func<T, bool>> func)
    {
        return _BaseRepository.Find(func);
    }

    public async Task<T> FindAsync(dynamic AId)
    {
        return await _BaseRepository.FindAsync(AId);
    }

    public async Task<T> FindAsync(Expression<Func<T, bool>> func)
    {
        return await _BaseRepository.FindAsync(func);
    }

    public bool Insert(T AEntity)
    {
        return _BaseRepository.Insert(AEntity);
    }

    public async Task<bool> InsertAsync(T AEntity)
    {
        return await _BaseRepository.InsertAsync(AEntity);
    }

    public async Task<bool> InsertRangeAsync(List<T> AList)
    {
        return await _BaseRepository.InsertRangeAsync(AList); ;
    }

    /// <summary>
    /// 查询
    /// </summary>
    /// <returns></returns>
    public List<T> Query()
    {
        return _BaseRepository.Query();
    }

    /// <summary>
    /// 自定义查询
    /// </summary>
    /// <param name="func"></param>
    /// <returns></returns>
    public List<T> Query(Expression<Func<T, bool>> func)
    {
        return _BaseRepository.Query(func);
    }

    public async Task<List<T>> QueryAsync()
    {
        return await _BaseRepository.QueryAsync();
    }

    public async Task<List<T>> QueryAsync(Expression<Func<T, bool>> func)
    {
        return await _BaseRepository.QueryAsync(func);
    }

    public async Task<List<T>> QueryAsync(int APageIndex, int APageSize, RefAsync<int> ATotal)
    {
        return await _BaseRepository.QueryAsync(APageIndex, APageSize, ATotal);
    }

    public async Task<List<T>> QueryAsync(Expression<Func<T, bool>> func, int APageIndex, int APageSize, RefAsync<int> ATotal)
    {
        return await _BaseRepository.QueryAsync(func, APageIndex, APageSize, ATotal);
    }

    /// <summary>
    /// 自定义条件分页查询
    /// </summary>
    /// <param name="func"></param>
    /// <param name="APageIndex"></param>
    /// <param name="APageSize"></param>
    /// <param name="ATotal"></param>
    /// <returns></returns>
    public async Task<List<T>> QueryAsync(Expression<Func<T, bool>> func, string orderByFields, int APageIndex, int APageSize, RefAsync<int> ATotal)
    {
        return await _BaseRepository.QueryAsync(func, orderByFields, APageIndex, APageSize, ATotal);
    }

    /// <summary>
    /// 自定义条件分页查询
    /// </summary>
    /// <param name="whereExpression"></param>
    /// <param name="orderByExpression"></param>
    /// <param name="order"></param>
    /// <param name="APageIndex"></param>
    /// <param name="APageSize"></param>
    /// <param name="ATotal"></param>
    /// <returns></returns>
    public async Task<List<T>> QueryAsync(Expression<Func<T, bool>> whereExpression, Expression<Func<T, object>> orderByExpression, OrderByType order, int APageIndex, int APageSize, RefAsync<int> ATotal)
    {
        return await _BaseRepository.QueryAsync(whereExpression, orderByExpression, order, APageIndex, APageSize, ATotal);
    }

    public bool Update(T AEntity)
    {
        return _BaseRepository.Update(AEntity);
    }

    public async Task<bool> UpdateAsync(T AEntity)
    {
        return await _BaseRepository.UpdateAsync(AEntity);
    }

    public async Task<bool> UpdateRangeAsync(List<T> AList)
    {
        return await _BaseRepository.UpdateRangeAsync(AList);
    }

    /// <summary>
    /// 开始事务
    /// </summary>
    /// <exception cref="NotImplementedException"></exception>
    public void BeginTran()
    {
        _BaseRepository.BeginTran();
    }

    /// <summary>
    /// 提交事务
    /// </summary>
    /// <exception cref="NotImplementedException"></exception>
    public void CommitTran()
    {
        _BaseRepository.CommitTran();
    }

    /// <summary>
    /// 回滚事务
    /// </summary>
    /// <exception cref="NotImplementedException"></exception>
    public void RollbackTran()
    {
        _BaseRepository.RollbackTran();
    }

    #region 执行sql

    /// <summary>
    /// 获取DataTable数据
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>DataTable</returns>
    public DataTable GetDataTable(string sql, object parameters)
    {
        return _BaseRepository.GetDataTable(sql, parameters);
    }

    /// <summary>
    /// 获取DataTable数据
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>DataTable</returns>
    public DataTable GetDataTable(string sql, params SugarParameter[] parameters)
    {
        return _BaseRepository.GetDataTable(sql, parameters);
    }

    /// <summary>
    /// 获取DataTable数据
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>DataTable</returns>
    public DataTable GetDataTable(string sql, List<SugarParameter> parameters)
    {
        return _BaseRepository.GetDataTable(sql, parameters);
    }

    /// <summary>
    /// 获取DataTable数据
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>DataTable</returns>
    public async Task<DataTable> GetDataTableAsync(string sql, object parameters)
    {
        return await _BaseRepository.GetDataTableAsync(sql, parameters);
    }

    /// <summary>
    /// 获取DataTable数据
    /// </summary>
    /// <param name="ASql"></param>
    /// <param name="parameters"></param>
    /// <returns>DataTable</returns>
    public async Task<DataTable> GetDataTableAsync(string ASql, params SugarParameter[] parameters)
    {
        return await _BaseRepository.GetDataTableAsync(ASql, parameters);
    }

    /// <summary>
    /// 获取DataTable数据
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>DataTable</returns>
    public async Task<DataTable> GetDataTableAsync(string sql, List<SugarParameter> parameters)
    {
        return await _BaseRepository.GetDataTableAsync(sql, parameters);
    }

    /// <summary>
    /// 获取DataSet数据
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>DataSet</returns>
    public DataSet GetDataSetAll(string sql, object parameters)
    {
        return _BaseRepository.GetDataSetAll(sql, parameters);
    }

    /// <summary>
    /// 获取DataSet数据
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>DataSet</returns>
    public DataSet GetDataSetAll(string sql, params SugarParameter[] parameters)
    {
        return _BaseRepository.GetDataSetAll(sql, parameters);
    }

    /// <summary>
    /// 获取DataSet数据
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>DataSet</returns>
    public DataSet GetDataSetAll(string sql, List<SugarParameter> parameters)
    {
        return _BaseRepository.GetDataSetAll(sql, parameters);
    }

    /// <summary>
    /// 获取DataSet数据
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>DataSet</returns>
    public async Task<DataSet> GetDataSetAllAsync(string sql, object parameters)
    {
        return await _BaseRepository.GetDataSetAllAsync(sql, parameters);
    }

    /// <summary>
    /// 获取DataSet数据
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>DataSet</returns>
    public async Task<DataSet> GetDataSetAllAsync(string sql, params SugarParameter[] parameters)
    {
        return await _BaseRepository.GetDataSetAllAsync(sql, parameters);
    }

    /// <summary>
    /// 获取DataSet数据
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>DataSet</returns>
    public async Task<DataSet> GetDataSetAllAsync(string sql, List<SugarParameter> parameters)
    {
        return await _BaseRepository.GetDataSetAllAsync(sql, parameters);
    }

    /// <summary>
    /// 获取DataReader数据
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>IDataReader</returns>
    public IDataReader GetDataReader(string sql, object parameters)
    {
        return _BaseRepository.GetDataReader(sql, parameters);
    }

    /// <summary>
    /// 获取DataReader数据
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>IDataReader</returns>
    public IDataReader GetDataReader(string sql, params SugarParameter[] parameters)
    {
        return _BaseRepository.GetDataReader(sql, parameters);
    }

    /// <summary>
    /// 获取DataReader数据
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>IDataReader</returns>
    public IDataReader GetDataReader(string sql, List<SugarParameter> parameters)
    {
        return _BaseRepository.GetDataReader(sql, parameters);
    }

    /// <summary>
    /// 获取DataReader数据
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>IDataReader</returns>
    public IDataReader GetDataReaderAsync(string sql, object parameters)
    {
        return await _BaseRepository.GetDataReaderAsync(sql, parameters);
    }

    /// <summary>
    /// 获取DataReader数据
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>IDataReader</returns>
    public async Task<IDataReader> GetDataReaderAsync(string sql, params SugarParameter[] parameters)
    {
        return await _BaseRepository.GetDataReaderAsync(sql, parameters);
    }

    /// <summary>
    /// 获取DataReader数据
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>IDataReader</returns>
    public async Task<IDataReader> GetDataReaderAsync(string sql, List<SugarParameter> parameters)
    {
        return await _BaseRepository.GetDataReaderAsync(sql, parameters);
    }

    /// <summary>
    /// 获取object数据
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>object</returns>
    public object GetScalar(string sql, object parameters)
    {
        return _BaseRepository.GetScalar(sql, parameters);
    }

    /// <summary>
    /// 获取object数据
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>object</returns>
    public object GetScalar(string sql, params SugarParameter[] parameters)
    {
        return _BaseRepository.GetScalar(sql, parameters);
    }

    /// <summary>
    /// 获取object数据
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>object</returns>
    public object GetScalar(string sql, List<SugarParameter> parameters)
    {
        return _BaseRepository.GetScalar(sql, parameters);
    }

    /// <summary>
    /// 获取object数据
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>object</returns>
    public async Task<object> GetScalarAsync(string sql, object parameters)
    {
        return await _BaseRepository.GetScalarAsync(sql, parameters);
    }

    /// <summary>
    /// 获取object数据
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>object</returns>
    public async Task<object> GetScalarAsync(string sql, params SugarParameter[] parameters)
    {
        return await _BaseRepository.GetScalarAsync(sql, parameters);
    }

    /// <summary>
    /// 获取object数据
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>object</returns>
    public async Task<object> GetScalarAsync(string sql, List<SugarParameter> parameters)
    {
        return await _BaseRepository.GetScalarAsync(sql, parameters);
    }

    /// <summary>
    /// 执行sql返回整型
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>int</returns>
    public int ExecuteCommandWithGo(string sql, params SugarParameter[] parameters)
    {
        return _BaseRepository.ExecuteCommandWithGo(sql, parameters);
    }

    /// <summary>
    /// 执行sql返回整型
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>int</returns>
    public int ExecuteCommand(string sql, object parameters)
    {
        return _BaseRepository.ExecuteCommand(sql, parameters);
    }

    /// <summary>
    /// 执行sql返回整型
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>int</returns>
    public int ExecuteCommand(string sql, params SugarParameter[] parameters)
    {
        return _BaseRepository.ExecuteCommand(sql, parameters);
    }

    /// <summary>
    /// 执行sql返回整型
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>int</returns>
    public int ExecuteCommand(string sql, List<SugarParameter> parameters)
    {
        return _BaseRepository.ExecuteCommand(sql, parameters);
    }

    /// <summary>
    /// 执行sql返回整型
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>int</returns>
    public async Task<int> ExecuteCommandAsync(string sql, params SugarParameter[] parameters)
    {
        return await _BaseRepository.ExecuteCommandAsync(sql, parameters);
    }

    /// <summary>
    /// 执行sql返回整型
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>int</returns>
    public async Task<int> ExecuteCommandAsync(string sql, object parameters)
    {
        return await _BaseRepository.ExecuteCommandAsync(sql, parameters);
    }

    /// <summary>
    /// 执行sql返回整型
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>int</returns>
    public async Task<int> ExecuteCommandAsync(string sql, List<SugarParameter> parameters)
    {
        return await _BaseRepository.ExecuteCommandAsync(sql, parameters);
    }

    /// <summary>
    /// 执行SQL返回自定义实体
    /// </summary>
    /// <typeparam name="T">实体对象</typeparam>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns></returns>
    public List<T> SqlQuery<T>(string sql, object parameters = null)
    {
        return _BaseRepository.SqlQuery<T>(sql, parameters);
    }

    /// <summary>
    /// 执行SQL返回自定义实体
    /// </summary>
    /// <typeparam name="T">实体对象</typeparam>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns></returns>
    public List<T> SqlQuery<T>(string sql, params SugarParameter[] parameters)
    {
        return _BaseRepository.SqlQuery<T>(sql, parameters);
    }

    /// <summary>
    /// 执行SQL返回自定义实体
    /// </summary>
    /// <typeparam name="T">实体对象</typeparam>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns></returns>
    public List<T> SqlQuery<T>(string sql, List<SugarParameter> parameters)
    {
        return _BaseRepository.SqlQuery<T>(sql, parameters);
    }

    /// <summary>
    /// 执行SQL返回自定义实体
    /// </summary>
    /// <typeparam name="T">实体对象</typeparam>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns></returns>
    public async Task<List<T>> SqlQueryAsync<T>(string sql, object parameters = null)
    {
        return await _BaseRepository.SqlQueryAsync<T>(sql, parameters);
    }

    /// <summary>
    /// 执行SQL返回自定义实体
    /// </summary>
    /// <typeparam name="T">实体对象</typeparam>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns></returns>
    public async Task<List<T>> SqlQueryAsync<T>(string sql, List<SugarParameter> parameters)
    {
        return await _BaseRepository.SqlQueryAsync<T>(sql, parameters);
    }

    /// <summary>
    /// 执行SQL返回自定义实体
    /// </summary>
    /// <typeparam name="T">实体对象</typeparam>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns></returns>
    public async Task<List<T>> SqlQueryAsync<T>(string sql, params SugarParameter[] parameters)
    {
        return await _BaseRepository.SqlQueryAsync<T>(sql, parameters);
    }

    /// <summary>
    /// 执行SQL返回自定义实体
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="whereObj"></param>
    /// <returns></returns>
    public T SqlQuerySingle<T>(string sql, object whereObj = null)
    {
        return _BaseRepository.SqlQuerySingle<T>(sql, whereObj);
    }

    /// <summary>
    /// 执行SQL返回自定义实体
    /// </summary>
    /// <param name="T">实体对象</typeparam>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns></returns>
    public T SqlQuerySingle<T>(string sql, params SugarParameter[] parameters)
    {
        return _BaseRepository.SqlQuerySingle<T>(sql, parameters);
    }

    /// <summary>
    /// 执行SQL返回自定义实体
    /// </summary>
    /// <typeparam name="T">实体对象</typeparam>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns></returns>
    public T SqlQuerySingle<T>(string sql, List<SugarParameter> parameters)
    {
        return _BaseRepository.SqlQuerySingle<T>(sql, parameters);
    }

    #endregion
}
```

### TestService.cs（业务实现示例）

```csharp
// Application/Services/TestService.cs
public class TestService : BaseService<Test>, ITestService
{
    private readonly ITestRepository _Repository;

    public TestService(ITestRepository repository)
    {
        base._BaseRepository = repository;
        _Repository = repository;
    }
}
```
