# Domain 层模板

> 摘自 dapr-dotnet 技能 v1.0.0「Domain」章节。包含：实体基类、实体示例、仓储接口基类。

## 一、BaseEntity.cs

```csharp
// Domain/SeedWork/BaseEntity.cs
/// <summary>
/// 实体基类
/// </summary>
public class BaseEntity
{
    /// <summary>
    /// 是否标记删除
    /// </summary>
    public bool IsDelete { get; set; } = false;

    /// <summary>
    /// 创建时间
    /// </summary>
    public DateTime CreateDateTime { get; set; } = DateTime.Now;

    /// <summary>
    /// 最后修改时间
    /// </summary>
    public DateTime LastupdateDateTime { get; set; } = DateTime.Now;
}
```

要点：`IsDelete` 为逻辑删除标记（默认 `false`）；两个时间字段带默认值，插入时无需显式赋值。

## 二、Test.cs（实体示例）

```csharp
// Domain/Models/Test.cs
/// <summary>
/// 
/// </summary>
[SugarTable("t_test")]
public class Test : BaseEntity
{
    /// <summary>
    /// 主键ID
    /// </summary>
    [SugarColumn(IsPrimaryKey = true, ColumnDescription = "主键")]
    public long Id { get; set; }
}
```

要点：实体必须继承 `BaseEntity`；用 `[SugarTable("表名")]` 映射表，主键用 `[SugarColumn(IsPrimaryKey = true)]` 标注。

## 三、IBaseRepository.cs

```csharp
// Domain/SeedWork/IBaseRepository.cs
/// <summary>
/// 仓储基类接口
/// </summary>
/// <typeparam name="T"></typeparam>
public interface IBaseRepository<T> where T : class, new()
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

## 四、ITestRepository.cs（业务仓储接口示例）

```csharp
// Domain/Repositories/ITestRepository.cs
public interface ITestRepository: IBaseRepository<Test>
{
}
```
